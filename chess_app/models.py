	# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Chessboard(models.Model):
	user_input_state = models.CharField(max_length=1000)
	current_player_type = models.CharField(null=True, blank=True, default="player", max_length=10)

	def __str__(self):
		return "Chessboard: %s"%self.pk

	def get_absolute_url(self):
		return reverse('chess_app:chess_detail', kwargs={'pk':self.pk})

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User, related_name='userprofileinfos', on_delete=models.CASCADE, blank=True, null=True, default=1)
	picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
	chessboard = models.ForeignKey(Chessboard, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('chess_app:profile_detail', kwargs={'pk':self.pk})
