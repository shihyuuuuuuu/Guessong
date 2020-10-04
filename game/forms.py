from django import forms

class AddSongForm(forms.Form):
    url = forms.URLField(
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': '請貼上歌曲 Youtube 連結',
            }
        )
    )
    song_name = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(
            attrs = {
                'placeholder': '請輸入歌曲名',
            }
        )
    )
    singer = forms.CharField(
        max_length=100,
        required=False,
        widget = forms.TextInput(
            attrs = {
                'placeholder': '請輸入歌手名',
            }
        )
    )

    def clean_url(self):
        return self.cleaned_data['url']
    
    def clean_song_name(self):
        return self.cleaned_data['song_name']
    
    def clean_singer(self):
        return self.cleaned_data['singer']
    