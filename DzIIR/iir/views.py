from django.shortcuts import render
from django.views import View

from .services import do_some_stuff
from .forms import EqualizerForm


image_list = [
    {'name': 'Входной сигнал', 'url': 'media/plots/input_signal.png'},
    {'name': 'Выходной сигнал', 'url': 'media/plots/output_signal.png'},

    {'name': 'АЧХ 1-фильтра', 'url': 'media/plots/1/fltr1.png'},
    {'name': 'АЧХ сигнала после 1-фильтра', 'url': 'media/plots/y1.png'},

    {'name': 'АЧХ 2-фильтра', 'url': 'media/plots/2/fltr2.png'},
    {'name': 'АЧХ сигнала после 2-фильтра', 'url': 'media/plots/y2.png'},

    {'name': 'АЧХ 3-фильтра', 'url': 'media/plots/3/fltr3.png'},
    {'name': 'АЧХ сигнала после 3-фильтра', 'url': 'media/plots/y3.png'},

    {'name': 'АЧХ 4-фильтра', 'url': 'media/plots/4/fltr4.png'},
    {'name': 'АЧХ сигнала после 4-фильтра', 'url': 'media/plots/y4.png'},

    {'name': 'АЧХ 5-фильтра', 'url': 'media/plots/5/fltr5.png'},
    {'name': 'АЧХ сигнала после 5-фильтра', 'url': 'media/plots/y5.png'},

    {'name': 'Суммарная АЧХ сигнала после фильтров', 'url': 'media/plots/y_sum.png'},
]


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        form = EqualizerForm()
        context = {'form': form}
        return render(request, 'index.html', context)

    def post(self, request):
        form = EqualizerForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            data = request.POST
            do_some_stuff(n1=int(data['eq1']),
                          n2=int(data['eq2']),
                          n3=int(data['eq3']),
                          n4=int(data['eq4']),
                          n5=int(data['eq5']))
            context['image_list'] = image_list
        return render(request, 'index.html', context)
