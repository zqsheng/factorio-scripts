#include <iostream>
#include <thread>
#include <semaphore>

std::binary_semaphore sema{0};

void task() {
    for(int i = 0; i < 199; i++) {
        std::cout << "task " << i << std::endl;
    }
    sema.release();
}

int main() {
    std::thread worker(task);
    sema.acquire();
    return 0;
}
clas
private:
    int n;
    volatile int counter;
    std::binary_semaphore sema_zero{1};
    std::binary_semaphore sema_even{0};
    std::binary_semaphore sema_odd{0};
public:
    ZeroEvenOdd(int n) {
        this->n = n;
        this->counter = 0;
    }

    void zero(function<void(int)> printNumber) {
        for(int i = 0; i < n; i++) {
            sema_zero.acquire();
            printNumber(0);
            counter++;
            if ((counter&1)) sema_odd.release();
            else sema_even.release();
        }
    }

    void odd(function<void(int)> printNumber) {
        for(int i = 0; i < (n+1)/2; i++) {
            sema_odd.acquire();
            printNumber(counter);
            sema_zero.release();
        }
    }

    void even(function<void(int)> printNumber) {
        for(int i = 0; i < n/2; i++) {
            sema_even.acquire();
            printNumber(counter);
            sema_zero.release();
        }
    }

}
class H2O {
public:
    std::counting_semaphore<10> sema_hyrogen{2};
    std::counting_semaphore<10> sema_oxygen{1};
    int counter_hyrogen = 0;

    
    H2O() { 
     }

    void hydrogen(function<void()> releaseHydrogen) {
        sema_hyrogen.acquire();
        releaseHydrogen();
        counter_hyrogen++;
        if (counter_hyrogen == 2) {
            counter_hyrogen = 0;
            sema_oxygen.release();
        }
        
    }

    void oxygen(function<void()> releaseOxygen) {
        
        sema_oxygen.acquire();
        // releaseOxygen() outputs "O". Do not change or remove this line.
        releaseOxygen();
        sema_hyrogen.release();
        sema_hyrogen.release();
    }
};;
class FizzBuzz {
private:
    int n;
    int x;
    
    std::counting_semaphore<4> sema_numb{1};
    std::counting_semaphore<4> sema_fizz{0};
    std::counting_semaphore<4> sema_buzz{0};
    std::counting_semaphore<4> sema_fibu{0};
    
public:
    FizzBuzz(int n) {
        this->n = n;
        this->x = 1;
    }
    void next() {
        x++;
        if (x%3==0 && x%5==0) {
            sema_fibu.release();
        } else if (x%3==0) {
            sema_fizz.release();
        } else if (x%5==0) {
            sema_buzz.release();
        } else {
            sema_numb.release();
        }
    }

    bool hasNext(function<bool(int)> predicate) {
        for(int y = x; y <= n; y++) {
            if (predicate(y)) return true;
        }
        return false;
    }
    
    

    // printFizz() outputs "fizz".
    void fizz(function<void()> printFizz) {
        while(hasNext([](int y) -> bool { return y%3==0 && y%5!=0;})) {
            sema_fizz.acquire();
            printFizz();
            next();
        }
    }

    // printBuzz() outputs "buzz".
    void buzz(function<void()> printBuzz) {
        while(hasNext([](int y) -> bool { return y%3!=0 && y%5==0;})) {
            sema_buzz.acquire();
            printBuzz();
            next();
        }
    }

    // printFizzBuzz() outputs "fizzbuzz".
	void fizzbuzz(function<void()> printFizzBuzz) {
        while(hasNext([](int y) -> bool { return y%3==0 && y%5==0;})) {
            sema_fibu.acquire();
            printFizzBuzz();
            next();
        }
    }

    // printNumber(x) outputs "x", where x is an integer.
    void number(function<void(int)> printNumber) {
        while(hasNext([](int y) -> bool { return y%3!=0 && y%5!=0;})) {
            sema_numb.acquire();
            printNumber(x);
            next();
        }
    }
};
type Foo struct {
        ch_second chan int
                ch_third chan int
}

func NewFoo() *Foo {
        return &Foo{ ch_second: make(chan int, 0),  ch_third: make(chan int, 0) }
}

func (f *Foo) First(printFirst func()) {
        printFirst();
            f.ch_second <- 1
}

func (f *Foo) Second(printSecond func()) {
        _ :<- f.ch_second
                printSecond()
                    f.ch_third <- 1
}

func (f *Foo) Third(printThird func()) {
        _ :<- f.ch_third
                printThird()
}
type FooBar struct {
	n int
    ch_foo chan int
    ch_bar chan int
}

func NewFooBar(n int) *FooBar {
    ch_foo, ch_bar := make(chan int, 1), make(chan int, 0)
    ch_foo <- 1
	return &FooBar{n: n, ch_foo: ch_foo, ch_bar: ch_bar}
}

func (fb *FooBar) Foo(printFoo func()) {
	for i := 0; i < fb.n; i++ {
        select { case <- fb.ch_foo: {} }
        printFoo()
        fb.ch_bar <- 1
	}
}

func (fb *FooBar) Bar(printBar func()) {
	for i := 0; i < fb.n; i++ {
        select { case <- fb.ch_bar: {} }
        printBar()
        fb.ch_foo <- 1
	}
}
type ZeroEvenOdd struct {
	n int
    x int
    ch_z chan int
    ch_e chan int
    ch_o chan int
}

func NewZeroEvenOdd(n int) *ZeroEvenOdd {
	zeo := &ZeroEvenOdd{ }
    zeo.n = n
    zeo.x = 0
    ch_z, ch_e, ch_o := make(chan int, 1), make(chan int, 0), make(chan int, 0)
    ch_z <- 1
    
    zeo.ch_z = ch_z
    zeo.ch_e = ch_e
    zeo.ch_o = ch_o
	return zeo
}

func (z *ZeroEvenOdd) Zero(printNumber func(int)) {
    for i := 0; i < z.n; i++ {
        <- z.ch_z 
        printNumber(0)
        z.x++
        if ((z.x&1) == 0) { 
            z.ch_e <- 1
        } else { 
            z.ch_o <- 1
        }
    }
}


func (z *ZeroEvenOdd) Even(printNumber func(int)) {
    for i := 0; i < z.n/2; i++ {
        <- z.ch_e
        printNumber(z.x)
        z.ch_z <- 1
    }
}

func (z *ZeroEvenOdd) Odd(printNumber func(int)) {
    for i := 0; i < (z.n+1)/2; i++ {
        <- z.ch_o
        printNumber(z.x)
        z.ch_z <- 1
    }

}
