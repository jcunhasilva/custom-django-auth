from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import RegisterPublicForm
from models import Profile, PublicProfile
from django.views.generic import CreateView, DetailView, View
from django.http import Http404


class AccountRegistration(CreateView):
    model = PublicProfile
    form_class = RegisterPublicForm
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return super(AccountRegistration, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = RegisterPublicForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            user.save()
            profile = Profile(user=user, name=form.cleaned_data['name'], 
                            gender=form.cleaned_data['gender'], hobbies=form.cleaned_data['hobbies'])
            profile.save()
          
            public_bio = form.cleaned_data['public_bio']
            if public_bio:
                public_profile = PublicProfile(profile=profile, public_bio=public_bio)
                public_profile.save()
        
            return HttpResponseRedirect('/')
        else:
            return render_to_response('profiles/publicprofile_form.html', {'form':form}, context_instance=RequestContext(request))

class ProfileView(DetailView):
    model = PublicProfile
    
    def get_object(self, queryset=None):      
        try:
            query_user = self.request.GET[u'username']
        except KeyError:
            query_user = None   
        
        if query_user:
            current_user = get_object_or_404(User.objects.filter(username=query_user))
        elif self.request.user.is_authenticated():
            current_user = self.request.user
        else:
            current_user = None
        
        if current_user:
            profile = current_user.get_profile()
        
            try:
                public_profile = get_object_or_404(PublicProfile.objects.filter(profile=profile))
            except Http404:
                if current_user == self.request.user:
                    public_profile = PublicProfile(profile=profile)
                else:
                    raise Http404
        else:
            public_profile = None

        return public_profile

class SearchView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            query_user = request.POST['query_user']
        except KeyError:
            return HttpResponseRedirect('/')
            
        return HttpResponseRedirect('/profile?username=%s' % query_user)
        
    