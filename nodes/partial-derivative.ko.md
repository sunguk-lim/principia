# 편미분

## 요약

**편미분(partial derivative)**은 다변수 함수가 나머지 입력은 고정한 채 **하나의**
입력만 움직일 때 어떻게 변하는지를 측정한다.

## 상세 설명

이는 그저 다른 변수들은 상수로 취급하면서 하나의 변수에 대해 취한 [[derivative]]일 뿐이다:

$$\frac{\partial f}{\partial x_i} = \lim_{h\to 0}\frac{f(\dots,x_i+h,\dots)-f(\dots,x_i,\dots)}{h}$$

이것들을 모두 쌓아 올린 것이 델 연산자, 기울기(그래디언트), 야코비안, 헤시안이
만들어지는 방식이다.

## 선행 개념

- [[derivative]]

## 출처

- etc/differential-operators-summary.html
