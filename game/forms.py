from django import forms

class AddSongForm(forms.Form):
    url = forms.URLField(required=True)
    song_name = forms.CharField(max_length=100, required=False)
    singer = forms.CharField(max_length=100, required=False)

    def clean_url(self):
        return self.cleaned_data['url']
    
    def clean_song_name(self):
        return self.cleaned_data['song_name']
    
    def clean_singer(self):
        return self.cleaned_data['singer']
    