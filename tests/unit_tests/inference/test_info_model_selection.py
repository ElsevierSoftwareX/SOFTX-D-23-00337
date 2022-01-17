from UQpy.inference.information_criteria import *
from UQpy.distributions.collection import Gamma, Exponential, ChiSquare
from UQpy.inference.inference_models.DistributionModel import DistributionModel
from UQpy.inference.InformationModelSelection import InformationModelSelection


def test_aic():
    data = Gamma(a=2, loc=0, scale=2).rvs(nsamples=500, random_state=12)

    m0 = DistributionModel(distributions=Gamma(a=None, loc=None, scale=None), n_parameters=3, name='gamma')
    m1 = DistributionModel(distributions=Exponential(loc=None, scale=None), n_parameters=2, name='exponential')
    m2 = DistributionModel(distributions=ChiSquare(df=None, loc=None, scale=None),
                           n_parameters=3, name='chi-square')

    candidate_models = [m0, m1, m2]
    selector = InformationModelSelection(candidate_models=candidate_models,
                                         data=data,
                                         criterion=AIC(),
                                         random_state=0)
    selector.run(optimizations_number=5)
    selector.sort_models()
    assert 2285.9685816790425 == selector.criterion_values[0]
    assert 2285.9685821390594 == selector.criterion_values[1]
    assert 2368.9477307542193 == selector.criterion_values[2]


def test_bic():
    data = Gamma(a=2, loc=0, scale=2).rvs(nsamples=500, random_state=12)
    m0 = DistributionModel(distributions=Gamma(a=None, loc=None, scale=None), n_parameters=3, name='gamma')
    m1 = DistributionModel(distributions=Exponential(loc=None, scale=None), n_parameters=2, name='exponential')
    m2 = DistributionModel(distributions=ChiSquare(df=None, loc=None, scale=None),
                           n_parameters=3, name='chi-square')

    candidate_models = [m0, m1, m2]

    selector = InformationModelSelection(candidate_models=candidate_models,
                                         data=data,
                                         criterion=BIC(),
                                         random_state=0)
    selector.run(optimizations_number=5)
    selector.sort_models()
    assert 0.5000000575021204 == selector.probabilities[0]
    assert 0.4999999424978796 == selector.probabilities[1]
    assert 3.939737591540338e-18 == selector.probabilities[2]


def test_aicc():
    data = Gamma(a=2, loc=0, scale=2).rvs(nsamples=500, random_state=12)
    m0 = DistributionModel(distributions=Gamma(a=None, loc=None, scale=None), n_parameters=3, name='gamma')
    m1 = DistributionModel(distributions=Exponential(loc=None, scale=None), n_parameters=2, name='exponential')
    m2 = DistributionModel(distributions=ChiSquare(df=None, loc=None, scale=None),
                           n_parameters=3, name='chi-square')

    candidate_models = [m0, m1, m2]
    selector = InformationModelSelection(candidate_models=candidate_models,
                                         data=data,
                                         criterion=AICc(),
                                         random_state=0)
    selector.run(optimizations_number=5)
    selector.sort_models()
    assert 2286.0169687758166 == selector.criterion_values[0]
    assert 2286.0169692358336 == selector.criterion_values[1]
    assert 2368.9718756234347 == selector.criterion_values[2]
