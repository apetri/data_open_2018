import numpy as np
from sklearn.externals import joblib

from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Iris

IRIS_TYPES = {
    -1: "NONE",
    0: "IRIS_SETOSA",
    1: "IRIS_VERSICOLOR",
    2: "IRIS_VIRGINICA"
}
model = joblib.load(f'../../models/iris_gbc.pkl')


class IndexView(generic.ListView):
    template_name = 'data/index.html'
    context_object_name = 'top_flowers'

    def get_queryset(self):
        """Return five flowers."""
        return Iris.objects.order_by('-iris_class')[:5]


def detail(request, flower_id):
    flower = get_object_or_404(Iris, pk=flower_id)
    iris_type = model.predict(np.asarray([flower.petal_height,
                                          flower.petal_width,
                                          flower.sepal_height,
                                          flower.sepal_width]).reshape(1, -1))
    iris_classification = IRIS_TYPES[iris_type[0]]
    return render(request, 'data/detail.html', {'flower': flower, 'pred': iris_classification})
