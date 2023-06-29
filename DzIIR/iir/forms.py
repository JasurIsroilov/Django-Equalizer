from django import forms


class EqualizerForm(forms.Form):
    eq1 = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '100', 'id': 'iir1_range',
               'class': 'form-range'}
    ), label='Первая полоса фильтра')

    eq2 = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '100', 'id': 'iir2_range',
               'class': 'form-range'}
    ), label='Вторая полоса фильтра')

    eq3 = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '100', 'id': 'iir3_range',
               'class': 'form-range'}
    ), label='Третья полоса фильтра')

    eq4 = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '100', 'id': 'iir4_range',
               'class': 'form-range'}
    ), label='Четвертая полоса фильтра')

    eq5 = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '100', 'id': 'iir5_range',
               'class': 'form-range'}
    ), label='Пятая полоса фильтра')
