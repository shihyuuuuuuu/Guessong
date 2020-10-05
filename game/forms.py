from django import forms

class AddSongForm(forms.Form):
    url = forms.URLField(
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Paste the youtube link of the song',
                'title': 'Paste the youtube link of the song'
            }
        )
    )
    song_name = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Input the song name',
                'title': 'Input the song name'
            }
        )
    )
    singer = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Input the singer name',
                'title': 'Input the singer name'
            }
        )
    )

    def clean_url(self):
        return self.cleaned_data['url']
    
    def clean_song_name(self):
        return self.cleaned_data['song_name']
    
    def clean_singer(self):
        return self.cleaned_data['singer']
    