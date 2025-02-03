import pytest

from pycnpj_cpf.core import cnpj_or_cpf_is_valid


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize(
    'value',
    [
        '492.711.290-08',
        '299.621.190-14',
        '205.936.010-25',
        '41821790057',
        '34445321052',
        '17168587048',
        '33.378.832/0001-03',
        '81.109.827/0001-30',
        '85.840.881/0001-01',
        '11.222.333/0001-81',
        '72.101.517/0001-88',
        '37.453.242/0001-40',
        '69408076000157',
        '42278632000161',
    ],
)
def test_positive_cnpj_or_cpf_is_valid(value):
    """Test positive for function cpf_or_cnpj_is_valid."""
    assert cnpj_or_cpf_is_valid(value)


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize(
    'value',
    [
        '',
        '0',
        '492.711.290-18',
        '299.621.190-34',
        '205.936.311-45',
        '41821799857',
        '34453213252',
        '123',
        'abcdeqweu',
        '1234567891023102312301230',
        '33.378.832/0021-73',
        '81.109.847/0001-45',
        '85.840.121/0001-01',
        '11.222.444/0001-81',
        '69408076010157',
        '42278632067161',
        '42278632067162',
        '43378532067161',
        '42278632067179',
    ],
)
def test_negative_cnpj_or_cpf_is_valid(value):
    """Test negative for function cpf_or_cnpj_is_valid."""
    assert not cnpj_or_cpf_is_valid(value)
