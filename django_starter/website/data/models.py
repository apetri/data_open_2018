from django.db import models

IRIS_TYPES = {
    -1: "UNCLASSIFIED",
    0: "IRIS_SETOSA",
    1: "IRIS_VERSICOLOR",
    2: "IRIS_VIRGINICA"
}


class IrisManager(models.Manager):
    def create_iris(self, petal_height, petal_width, sepal_height, sepal_width):
        iris = self.create(petal_height=petal_height, petal_width=petal_width,
                           sepal_height=sepal_height, sepal_width=sepal_width)
        return iris


class Iris(models.Model):
    UNCLASSIFIED = -1
    IRIS_SETOSA = 0
    IRIS_VERSICOLOR = 1
    IRIS_VIRGINICA = 2
    petal_height = models.FloatField(default=0)
    petal_width = models.FloatField(default=0)
    sepal_height = models.FloatField(default=0)
    sepal_width = models.FloatField(default=0)
    iris_class = models.IntegerField(choices=(
        (UNCLASSIFIED, 'UNCLASSIFIED'),
        (IRIS_SETOSA, 'IRIS_SETOSA'),
        (IRIS_VERSICOLOR, 'IRIS_VERSICOLOR'),
        (IRIS_VIRGINICA, 'IRIS_VIRGINICA')), default=-1)

    def __str__(self):
        return "{}: Petal Height: {}, Petal Width: {}, Sepal Height: {}, Sepal Width: {} " \
            .format(IRIS_TYPES[self.iris_class], self.petal_height, self.petal_width,
                    self.sepal_height, self.sepal_width)

    objects = IrisManager()

    class Meta:
        verbose_name_plural = "irises"
