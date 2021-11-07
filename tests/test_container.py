from types import SimpleNamespace
import math

import numpy as np
from common import assert_close

from millipede.containers import SimpleSampleContainer, StreamingSampleContainer


def test_containers(P=101):
    c1 = SimpleSampleContainer()
    c2 = StreamingSampleContainer()

    for _ in range(4):
        gamma = np.random.binomial(1, 0.5 * np.ones(P))
        beta = np.random.randn(P)
        sample = SimpleNamespace(gamma=gamma,
                                 beta=beta * np.array(gamma, dtype=beta.dtype),
                                 add_prob=np.random.rand(P),
                                 log_nu=np.random.randn(),
                                 weight=np.random.rand())
        c1(sample)
        c2(sample)

    assert_close(c1.pip, c2.pip, atol=1.0e-12)
    assert_close(c1.beta, c2.beta, atol=1.0e-12)
    assert_close(c1.conditional_beta, c2.conditional_beta, atol=1.0e-12)

    for p in range(P):
        beta = c1.samples.beta[:, p]
        nz = np.nonzero(beta)[0]
        beta = beta[nz]
        weight = c1.samples.weight[nz]

        beta_mean = (np.sum(weight * beta) / np.sum(weight)).item() if len(beta) > 0 else 0.0
        expected = beta_mean if len(beta) > 0 else 0.0
        assert_close(c1.conditional_beta[p].item(), expected)

        beta_var = (np.sum(np.square(beta) * weight) / np.sum(weight)).item() - beta_mean ** 2 if len(beta) > 0 else 0.0
        expected = math.sqrt(np.clip(beta_var, a_min=0.0, a_max=None)) if len(beta) > 0 else 0.0
        assert_close(c1.conditional_beta_std[p].item(), expected)

    assert_close(c1.log_nu, c2.log_nu, atol=1.0e-12)
    assert_close(c1.log_nu_std, c2.log_nu_std, atol=1.0e-12)
    assert_close(c1.nu, c2.nu, atol=1.0e-12)
    assert_close(c1.nu_std, c2.nu_std, atol=1.0e-12)
    assert_close(c1.beta_std, c2.beta_std, atol=1.0e-12)
