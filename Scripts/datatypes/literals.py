from typing import Literal, TypeAlias

TimePeriod: TypeAlias = Literal['aht','pt','iht']
TimePeriodDay: TypeAlias = Literal['aht','pt','iht','vrk']
ModeCharacter: TypeAlias = Literal['h','c','v','k','y','b','g','d','e','t','p','r','j','m','a','s','f','w']
ImpedanceType: TypeAlias = Literal['dist','time','cost']
PurposeType: TypeAlias = Literal['hw','hs','hc','hu','ho','hh','hoo','wh','hwp','hop','sop','oop','external']
EmmeMatrixType: TypeAlias = Literal['demand','time','dist','cost','gen_cost','congest_time']
