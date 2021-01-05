from .adversarial_loss import WGANCriterion, RGANCriterion, RaGANCriterion
from .build import CRITERION_REGISTRY
from .loss import GradientPenalty, EpsilonPenalty, PosePredictionPenalty, L1Loss
from .optimizer import LossOptimizer
