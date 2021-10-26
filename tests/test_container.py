from types import SimpleNamespace

import numpy as np
from common import assert_close

from millipede.containers import SimpleSampleContainer, StreamingSampleContainer


def test_containers(P=5):
    c1 = SimpleSampleContainer()
    c2 = StreamingSampleContainer()

    for _ in range(4):
        sample = SimpleNamespace(gamma=np.random.binomial(1, 0.5 * np.ones(P)),
                                 beta=np.random.randn(P),
                                 add_prob=np.random.rand(P),
                                 weight=np.random.rand())
        c1(sample)
        c2(sample)

    assert_close(c1.pip, c2.pip)
    assert_close(c1.beta, c2.beta)
    assert_close(c1.conditional_beta, c2.conditional_beta)