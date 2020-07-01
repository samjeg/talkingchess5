from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Chessboard, UserProfileInfo
from array import array


class UserCreateForm(UserCreationForm):

	class Meta:
		fields = ("username", "password1", "password2")
		model = get_user_model()

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields["username"].label = "Username:"
		self.fields["username"].help_text = None
		self.fields["password1"].help_text = None
		self.fields["password2"].help_text = None


class ChessboardForm(forms.ModelForm):
	matrix = [
		["comp_rook1", "comp_horse1", "comp_bishop1", "comp_queen", "comp_king", "comp_bishop2", "comp_horse2", "comp_rook2"],
		[ "comp_pawn1", "comp_pawn2", "comp_pawn3", "comp_pawn4", "comp_pawn5", "comp_pawn6", "comp_pawn7", "comp_pawn8" ],
		[ "", "", "", "", "", "", "", ""],
		[ "", "", "", "", "", "", "", ""],
		[ "", "", "", "", "", "", "", ""],
		[ "", "", "", "", "", "", "", ""],
		[ "player_pawn1", "player_pawn2", "player_pawn3", "player_pawn4", "player_pawn5", "player_pawn6", "player_pawn7", "player_pawn8" ],
		["player_rook1", "player_horse1", "player_bishop1", "player_queen", "player_king", "player_bishop2", "player_horse2", "player_rook2"]
	]

	user_input_state = forms.CharField(initial=matrix)

	class Meta:
		fields = ("user_input_state",)
		model = Chessboard

	def __init__(self, *args, **kwargs):
		super(ChessboardForm, self).__init__(*args, **kwargs)
		self.fields['user_input_state'].widget.attrs['id'] = 'input_state'
				

