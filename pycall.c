/*本代码为 定义 int add(int a, int b) 函数 ，返回a+b的数*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int Add(int a, int b) {
	printf("\n1-二数相加：a=%d b= %d\n", a, b);
	return a + b;
}

int Sub(int a, int b) {
	printf("\n2-二数相减：a=%d b= %d\n", a, b);
	return a - b;
}

int Mul(int a, int b) {
	printf("\n3-二数相乘：a=%d b= %d\n", a, b);
	return a * b;
}


int  Div(int a, int b) {
	printf("\n4-二数相除：a=%d b= %d\n", a, b);

	if (b != 0)
		return  a / b;
	else {
		printf("\n分母不能为0 !\n");
		return -9999;
	}

}

int Rem(int a, int b) {
	printf("\n5-二数求余:a=%d b= %d\n", a, b);

	if (b != 0)
		return a % b;
	else {
		printf("\n分母不能为0 !\n");
		return -9999;
	}
}

long long unsigned Fac( int  a) {
	printf("\n6-阶乘:a=%d\n ", a);

	long long unsigned k = 1, s = 1 ;

	if (a >= 0 && a <= 10) {
		if (a == 0 || a == 1)
			return 1 ;

		for  (k = 1; k <= a ; k++) {

			s = s * k ;
//			printf("s=%llu\n", s)	;
		}

		return s;
	} else {
		printf("\n只能计算(0-10）以内的阶乘\n");
		return -9999;
	}


}



// 函数用于判断一个整数是否为素数
bool isPrime(long long unsigned num) {
	if (num <= 1) {
		return false; // 1和负数不是素数
	}

	if (num <= 3) {
		return true; // 2和3是素数
	}

	if (num % 2 == 0 || num % 3 == 0) {
		return false; // 能被2或3整除的不是素数
	}

	for (int i = 5; i * i <= num; i += 6) {

		if (num % i == 0 || num % (i + 2) == 0) {
			return false; // 如果能被5及比5大2的整数整除，就不是素数
		}
	}

	return true; // 如果都不满足以上条件，则是素数
}



int main() {
	int bj = 0 ;
	long long unsigned k = 10000000001 ;

	printf("1-二数相加:%d\n", Add(18, 7));
	printf("2-二数相减:%d\n", Sub(18, 7));
	printf("3-二数相乘:%d\n", Mul(18, 7));
	printf("4-二数相除:%f\n", Div(18, 7));
	printf("5-二数求余:%d\n", Rem(18, 7));
	printf("6-阶乘:%llu\n", Fac(5));
	printf("6-阶乘:%llu\n", Fac(20));

	if  (isPrime(k))
		bj = 1;

	printf("7-素性检查:%llu  %s\n", k, ((bj == 1) ? "是素数" : "不是素数" ));

	printf("=====================================\n");


}




/***gcc -o libpycall.so -shared -fPIC pycall.c*/
