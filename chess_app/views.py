    # -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
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
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import models
from . import forms
from .ChessEngine.RobotMovement import RobotMovement
from .ChessEngine.ChessPieces.ChessPiece import ChessPiece 
import ast
import json

old_state = [
    ["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
    ["comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
    ["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
]

for i in range(8):
    for j in range(8):
        old_state[i][j] = old_state[i][j].encode("utf-8")

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
        return reverse_lazy('chess_app:chess_detail', kwargs={'pk':chess_detail_id})


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        profiles = models.UserProfileInfo.objects.all()
        chessboards = models.Chessboard.objects.all()
        user = self.request.user
        form = self.get_form()
        if user.is_authenticated:
            for profile in profiles:          
                if user.id == profile.user.id:
                    
                    context['profile_detail'] = profile
                    context['chess_form'] = form                   
                    for chessboard in chessboards:
                        if profile.chessboard == chessboard:
                            context["chess_detail"] = chessboard
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request.user.id)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, user_id):
        global chess_detail_id
        profiles = models.UserProfileInfo.objects.all()
        chessboard = models.Chessboard(
            user_input_state = form.cleaned_data['user_input_state']
        )

        for profile in profiles:          
            if user_id == profile.user.id:    
                profile.chessboard = chessboard
                 
                chessboard.save()
                profile.save()

        chess_detail_id = chessboard.id
        
        return super(IndexView, self).form_valid(form)



class UserProfileDetailView(FormMixin, DetailView):
    model = models.UserProfileInfo
    template_name = 'chess_app/profile_detail.html'
    form_class = forms.ChessboardForm
    chessdetail_id = 0


    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        form = self.get_form()
        chessboards = models.Chessboard.objects.all()
        profiles = models.UserProfileInfo.objects.all()
        context['profile_detail'] = self.get_object()
        
        if user.is_authenticated:
            for profile in profiles:
                if user.id == profile.user.id:
                    context['chess_form'] = form
                    for chessboard in chessboards:
                        if profile.chessboard == chessboard.id:
                            context["chess_detail"] = chessboard
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = models.Chessboard()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # global chessdetail_id
        chessboard = models.Chessboard(
            player = form.cleaned_data['user_input_state'],
        )

        chessboard.save()

        chessdetail_id = chessboard.id
        

        return redirect('chess_app:chess_detail', pk=chessdetail_id)

class UserProfileCreateView(CreateView):
    fields = ('user', 'picture', 'chessboard')
    model = models.UserProfileInfo
    template_name = 'chess_app/profile_create.html'

    def get_success_url(self):
        return reverse_lazy('chess_app:profile_detail', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(UserProfileCreateView, self).get_context_data(**kwargs)
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

    def robotCanMove(self, type_of_player, matrix, new_matrix):
        original_positions = []
        new_positions = []
        counter = 0
        s = set()
        chess_piece = ChessPiece()
          
        # get all the player pieces in original state
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if chess_piece.isType(matrix[i][j], type_of_player):
                    original_positions.append(chess_piece.id_gen(i, j))
                
            
        # get all the player pieces in the new state
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                if chess_piece.isType(new_matrix[i][j], type_of_player):
                    new_positions.append(chess_piece.id_gen(i, j))
        
    
        # count the positions that are the same 
        for i in range(len(original_positions)):
            for j in range(len(new_positions)):
                if j not in s: 
                    if original_positions[i] == new_positions[j]:
                        s.add(j)
                        counter += 1

        print("view chessboard detail orig pos %s new pos %s"%(len(original_positions), len(new_positions)))

        return len(original_positions) - 1 == counter

    
    def get_success_url(self):
        return reverse_lazy('chess_app:chess_detail', kwargs={'pk':self.object.pk})

    # user passes state which is changed by the ai the 
    # return state is passed to the front-end as context
    def get_context_data(self, **kwargs):
        global old_state 
        
        context = super(ChessboardDetailView, self).get_context_data(**kwargs)

        user = self.request.user
        profiles = models.UserProfileInfo.objects.all()

        self.object = self.get_object() 
        
        form = self.get_form()
        chessboard = models.Chessboard.objects.get(pk=self.object.id)
        chess_form = forms.ChessboardForm(instance=chessboard)
        robot = RobotMovement()
        if user.is_authenticated:
            chess_data = chessboard.user_input_state
            chess_data = ast.literal_eval(chess_data)

            if self.robotCanMove("player", old_state, chess_data):
                context['state'] = self.robot.playRandomMove(chess_data)
                old_state = self.robot.playRndomMove(chess_data)

            for profile in profiles:    
                if user.id == profile.user.id:
                    context['profile_detail'] = profile
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
        profile = models.UserProfileInfo.objects.get(user=request.user)
        profile_form = forms.UserProfileInfoForm(request.POST, instance=profile)
        if chess_form_has_data:
            if chess_form.is_valid() and profile_form.is_valid():
                return self.chess_form_valid(chess_form, chess_item, profile_form, profile)
            else:
                return self.form_invalid(chess_form)


    def chess_form_valid(self, chess_form, chess_item, profile_form, profile):
        if chess_item:
            # context = self.get_context_data(**kwargs)
            self.chess_state = chess_form.cleaned_data['user_input_state']
            chess_item = chess_form.save(commit=False)
            chess_item.user_input_state = chess_form.cleaned_data['user_input_state']
            chess_item.save()
            chess_instance = models.Chessboard.objects.get(pk=chess_item.pk)
            
            if profile:
                profile = profile_form.save(commit=False)
                profile.chessboard = chess_instance
                profile.save()  
            
        
        return super(ChessboardDetailView, self).form_valid(chess_form)




