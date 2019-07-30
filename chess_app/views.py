# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.urls import reverse
from django import forms as django_forms
from django.views.generic import (
									TemplateView, 
									DetailView,
									CreateView,
									UpdateView,
									DeleteView,
									ListView,
								)
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from . import models
from . import forms

class ChessBaseView(object):
	def __init__(self):
		self.chess_state = None


class Register(CreateView):
    form_class = forms.UserCreateForm
    template_name = "chess_app/register.html"
    success_url = reverse_lazy("index")

# home page view 
class IndexView(FormMixin, TemplateView):
	template_name = 'chess_app/index.html'
	model = models.Chessboard
	form_class = forms.ChessboardForm
	chess_detail_id = 0

	def get_success_url(self):
		# global chess_detail_id

		return reverse_lazy('chess_app:chess_detail', kwargs={'pk':chess_detail_id})


	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		profiles = models.UserProfileInfo.objects.all()
		chessboards = models.Chessboard.objects.all()
		user = self.request.user
		form = self.get_form()
		if user.is_authenticated:
			form.fields['player'].widget = django_forms.HiddenInput()
			form.initial['player'] = user.id
			form.fields['user_input_state'].widget = django_forms.HiddenInput()
			form.initial['user_input_state'] = "orange"
			context['chess_form'] = form
			for profile in profiles:
				if user.id == profile.user.id:
					context['profile_detail'] = profile
					for chessboard in chessboards:
						if profile.id == chessboard.player.id:
							context["chess_detail"] = chessboard
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		global chess_detail_id

		chessboard = models.Chessboard(
			player = form.cleaned_data['player'],
			user_input_state = form.cleaned_data['user_input_state'],
		)

		chessboard.save()

		chess_detail_id = chessboard.id
		
		return super(IndexView, self).form_valid(form)



class UserProfileDetailView(FormMixin, DetailView):
	model = models.UserProfileInfo
	template_name = 'chess_app/profile_detail.html'
	form_class = forms.ChessboardForm
	chessdetail_id = 0


	def get_context_data(self, **kwargs):
		# global chessdetail_id

		context = super(UserProfileDetailView, self).get_context_data(**kwargs)
		user = self.request.user
		form = self.get_form()
		chessboards = models.Chessboard.objects.all()
		profiles = models.UserProfileInfo.objects.all()
		# chessdetail_id = 0
		# context['chess_detail_id'] = chessdetail_id
		context['profile_detail'] = self.get_object()
		if user.is_authenticated:
			form.fields['player'].widget = django_forms.HiddenInput()
			form.initial['player'] = user.id
			form.fields['user_input_state'].widget = django_forms.HiddenInput()
			form.initial['user_input_state'] = "orange"
			context['chess_form'] = form
			for profile in profiles:
				if user.id == profile.user.id:
					for chessboard in chessboards:
						if profile.id == chessboard.player.id:
							context["chess_detail"] = chessboard
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = models.Chessboard()
		print("post")
		form = self.get_form()
		if form.is_valid():
			print("form valid")
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		# global chessdetail_id
		chessboard = models.Chessboard(
			player = form.cleaned_data['player'],
			user_input_state = form.cleaned_data['user_input_state'],
		)

		chessboard.save()

		chessdetail_id = chessboard.id
		
		print("saved form")

		return redirect('chess_app:chess_detail', pk=chessdetail_id)

class UserProfileCreateView(CreateView):
    fields = ('user', 'picture',)
    model = models.UserProfileInfo
    template_name = 'chess_app/profile_create.html'

    def get_success_url(self):
        return reverse_lazy('chess_app:profile_detail', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(UserProfileCreateView, self).get_context_data(**kwargs)
        print("Hello")
        profiles = models.UserProfileInfo.objects.all()
        user = self.request.user
        form = self.get_form()
        if user.is_authenticated:
            form.fields['user'].widget = django_forms.HiddenInput()
            form.initial['user'] = user.id
            context['profile_form'] = form
            for profile in profiles:
                if user.id == profile.user.id:
                    context['profile_detail'] = profile

        return context

class UserProfileUpdateView(UpdateView):
    fields = ('picture',)
    model = models.UserProfileInfo
    template_name = 'chess_app/profile_create.html'

    def get_success_url(self): 
        return reverse_lazy('chess_app:profile_detail', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        profiles = models.UserProfileInfo.objects.all()
        user = self.request.user
        form = self.get_form()
        if user.is_authenticated:
            context['profile_form'] = form
            for profile in profiles:
                if user.id == profile.user.id:
                    context['profile_detail'] = profile


        return context

# view for the chessboard 
class ChessboardDetailView(FormMixin, DetailView):
	model = models.Chessboard
	template_name = 'chess_app/chessboard.html'
	form_class = forms.ChessboardForm

	
	def get_success_url(self):
		return reverse_lazy('chess_app:chess_detail', kwargs={'pk':self.object.pk})

	# user passes state which is changed by the ai the 
	# return state is passed to the front-end as context
	def get_context_data(self, **kwargs):
		context = super(ChessboardDetailView, self).get_context_data(**kwargs)
		user = self.request.user
		profiles = models.UserProfileInfo.objects.all()
		self.object = self.get_object() 
		chessboard = models.Chessboard.objects.get(pk=self.object.id)
		form = self.get_form()
		chess_form = chess_form = forms.ChessboardForm(instance=chessboard)
		if user.is_authenticated:
			chess_data = chessboard.user_input_state
			print("Hi context: %s"%chessboard.user_input_state)
			if chess_data == "green_btn":
				context['state'] = "Apple"
			else:
				context['state'] = "Grape"
			for profile in profiles:	
				if user.id == profile.user.id:
					context['profile_detail'] = profile
					form.initial['player'] = user.id
					form.fields['player'].widget = django_forms.HiddenInput()
					context['chess_form'] = form
		return context


	def post(self, request, *args, **kwargs):
		chess_form_has_data = None
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object() 
		chess_item = models.Chessboard.objects.get(pk=self.object.id)
		chess_form = forms.ChessboardForm(request.POST, instance=chess_item)
		chess_form_has_data = chess_form.data.get('user_input_state')
		if chess_form_has_data:
			if chess_form.is_valid():
				return self.chess_form_valid(chess_form, chess_item)
			else:
				return self.form_invalid(chess_form)


	def chess_form_valid(self, chess_form, chess_item):
		
		if chess_item:
			self.chess_state = chess_form.cleaned_data['user_input_state']
			chess_item = chess_form.save(commit=False)
			chess_item.user_input_state = chess_form.cleaned_data['user_input_state']
			chess_item.save()
		
		return super(ChessboardDetailView, self).form_valid(chess_form)




