from turbo_ml.utils import options
from turbo_ml.base import Model
from sklearn.utils import all_estimators
from typing import Dict, Type
sklearn_models: Dict[str, Type[Model]] = {}


def _train(self: Model, data, target):
    self.model.fit(data, target)


def _predict(self: Model, data):
    return self.model.predict(data)


def _classifier_init(self: Model, **kwargs):
    self.model = self.classifier(**kwargs)


for name, classifier in all_estimators(type_filter='classifier'):
    try:
        classifier_obj = classifier()
        model = type(name, (Model,),
                     {'classifier': classifier, 'train': _train, 'predict': _predict, '__init__': _classifier_init})
        sklearn_models[name] = model
    except TypeError as e:
        pass

if __name__ == '__main__':
    from datasets import get_iris, get_breast_cancer
    # from datasets import get_iris
    # data, target = get_iris()
    # data['target'] = target
    # train_data = data.sample(120)
    # train_target = train_data.pop('target')
    # test_set = data.sample(30)
    # test_target = test_set.pop('target')
    # model = models.get('RandomForestClassifier')()
    # model.train(train_data, train_target)
    # print(model.predict(test_set) == test_target)
    # print(len(models))
    # print('-'*50)
    # print(models.keys())
    from turbo_ml.meta_learning.model_prediction import HyperTuner, StatisticalParametersExtractor
    for data, target in [get_breast_cancer(), get_iris()]:
        extractor = StatisticalParametersExtractor(data, target)
        characteristics = extractor.describe_dataset()
        print(characteristics)
        tuner = HyperTuner()
        for name, model in sklearn_models.items():
            print(name)
            hparams = {}
            hparams = tuner.optimize_hyperparameters(model, (data, target), 'classification',
                                                     no_classes=characteristics.num_classes, no_variables=characteristics.target_features, device=options.device, trials=50, thread_num=options.threads)
            print(hparams)
            model_instance = model(**hparams)
            model_instance.train(data, target)
            print(sum(model_instance.predict(data)
                  == target)/len(target))
