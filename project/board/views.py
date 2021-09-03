from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from .filters import ReactionFilter
from django.core.exceptions import PermissionDenied
from django.utils.crypto import get_random_string
from django.contrib import messages

from .models import Post, Reaction, OneTimeCode, Profile
from .forms import PostForm, SignUpForm, ReactionForm


class PostsView(ListView):
    model = Post
    template_name = 'board.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    reaction_form = ReactionForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['reaction_form'] = ReactionForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        user = Profile.objects.get(pk=self.request.user.id)
        new_reaction = Reaction(text=request.POST.get('text'), rUser=user, rPost=self.get_object())
        new_reaction.save()
        return redirect('/my_reactions/')


class PostWRDetailView(DetailView):
    model = Post
    template_name = 'postwr.html'
    context_object_name = 'postwr'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = {**super().get_context_data(*args, **kwargs)}
        instance = self.get_object()
        context['reactions'] = instance.reaction_set.all().order_by('-dateCreation')
        return context


# создание поста
class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = ('board.add_post')
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):  # это вряд ли работает адекватно, но по-другому не работает
        author = Profile.objects.get(pk=self.request.user.id)
        form.instance.postAuthor = author
        return super().form_valid(form)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm
    permission_required = 'board.change_post'

    def get_object(self,
                   **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.postAuthor.user != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    # permission_required = ('news.delete_post')
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/board/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        author = Profile.objects.get(pk=self.request.user.id)
        if obj.postAuthor.user != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(PostDelete, self).dispatch(request, *args, **kwargs)


class BoardLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'


class BoardLoginView(LoginView):
    template_name = 'login.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                v_code = OneTimeCode.objects.create(code=get_random_string(length=32), user=user)
                mail_subject = 'Активируйте вашу учетную запись!'
                message = render_to_string('verification_email.html', {
                    'user': user,
                    'code': v_code,
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return redirect('/verification/')
            else:
                messages.error(request, 'Вы сделали что-то не так')
                return render(request, 'signup.html', {'form': form})
        else:
            messages.error(request, 'Вы сделали что-то не так')
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        if OneTimeCode.objects.filter(code=code, user__email=email).exists():
            user = User.objects.get(email=email)
            authors_group = Group.objects.get(name='Authors')
            authors_group.user_set.add(user)
            login(request, user)
            return redirect('/board/')

        else:
            messages.warning(request, 'Неверный код активации')
            return render(request, 'verification.html')

    else:
        return render(request, 'verification.html')


@login_required()
def profile(request):
    return render(request, 'profile.html')


@login_required()
def reactions_to_my_posts(request):
    user_id = request.user.id
    username = request.user.username
    posts = Post.objects.filter(postAuthor__user__username=username)
    reactions = Reaction.objects.filter(rPost__in=posts)
    f = ReactionFilter(request.GET, queryset=reactions)
    context = {'reactions': reactions, 'filter': f, 'posts': posts}
    return HttpResponse(render_to_string('reactions.html', context, request))


@login_required()
def my_reactions(request):
    user_id = request.user.id
    my_reactions = Reaction.objects.filter(rUser__user__id=user_id)
    context = {'my_reactions': my_reactions}
    return HttpResponse(render_to_string('my_reactions.html', context, request))


@login_required()
def delete_reaction(request, **kwargs):
    pk = kwargs.get('pk')
    reaction = Reaction.objects.get(id=pk)
    posts = Post.objects.filter(postAuthor__user__id=request.user.id)
    if reaction in Reaction.objects.filter(rPost__in=posts):
        reaction.delete()
        return redirect('/reactions/')
    else:
        raise PermissionDenied


@login_required()
def accept(request, **kwargs):
    pk = kwargs.get('pk')
    reaction = Reaction.objects.get(id=pk)
    posts = Post.objects.filter(postAuthor__user__id=request.user.id)
    if reaction in Reaction.objects.filter(rPost__in=posts):
        reaction.accepted = True
        reaction.save()  # вот без этого вообще нельзя
        return redirect('/reactions/')

# Create your views here.
