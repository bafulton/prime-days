from math import sqrt, ceil, floor
from calendar import Calendar


def getPrimeBirthdays(birthday):
    p = PrimesGenerator()
    primeYears = []

    for i in range(0, 100):
        date = birthday + i
        if (p.checkPrime(date)):
            primeYears.append(int(date-10000*floor(date/10000)))

    return primeYears


def getPrimeDays(year):
    p = PrimesGenerator()

    primes = []
    cal = Calendar()
    multiple = int("1" + "0"*(len(str(year))))
    for month in range(1, 12):
        for day in cal.itermonthdays(year, month):
            # itermonthdays tacks on (to the month front/back) days necessary to get a full week, all represented as 0's
            if day is 0:
                continue

            num = month*100*multiple + day*multiple + year
            if p.checkPrime(num):
                primes.append("%(month)s/%(day)s/%(year)s" % {"month": month, "day": day, "year": year})

    return primes


class PrimesGenerator():
    primes = [2]
    current = 3

    def advancePrimes(self, endNum, nth=False):
        """Check all numbers up to the specified number or nth prime"""
        if nth:
            while len(self.primes) < endNum:
                self.calculate()
        else:
            while self.current <= endNum:
                self.calculate()

    def calculate(self):
        """Look at the current number and see if it's prime"""
        for p in self.primes:
            if self.current % p == 0:
                break
        else:
            # loop ran through list without finding a factor
            self.primes.append(self.current)

        # go to the next odd integer
        self.current += 2

    def checkPrime(self, num, showDivisors=False):
        """Check if a specified number is prime--simple (print true/false)"""
        if ceil(sqrt(num))+1 > self.current:
            # advance the list of primes before checking the number
            self.advancePrimes(ceil(sqrt(num))+1)

        divisors = []
        isPrime = True
        for p in self.primes:
            # exit if we've searched far enough
            if p > int(ceil(sqrt(num)))+1:
                break

            if num % p == 0:
                isPrime = False
                divisors.append(p)

                if not showDivisors:
                    break

        if showDivisors:
            return divisors
        else:
            return isPrime

    def getPrimes(self, n):
        """Get the all primes up to n"""
        if self.current < n:
            # advance the list of primes before checking the number
            self.advancePrimes(n)

        if len(self.primes) < 500:
            return self.primes
        else:
            count = 0
            for p in self.primes:
                if p <= n:
                    count += 1
                else:
                    break
            return "There are %d primes less than or equal to %d." % (count, n)

    def nthPrime(self, n):
        """Find the nth prime number"""
        if len(self.primes) < n:
            # advance the list of primes before checking the number
            self.advancePrimes(n, True)

        #print the last prime
        return self.primes[n-1]


# allows the use of VERY large ranges
# found here: http://stackoverflow.com/questions/1482480/xrange2100-overflowerror-long-int-too-large-to-convert-to-int
class MyXRange(object):
    def __init__(self, a1, a2=None, step=1):
        if step == 0:
            raise ValueError("arg 3 must not be 0")
        if a2 is None:
            a1, a2 = 0, a1
        if (a2 - a1) % step != 0:
            a2 += step - (a2 - a1) % step
        if cmp(a1, a2) != cmp(0, step):
            a2 = a1
        self.start, self.stop, self.step = a1, a2, step

    def __iter__(self):
        n = self.start
        while cmp(n, self.stop) == cmp(0, self.step):
            yield n
            n += self.step

    def __repr__(self):
        return "MyXRange(%d,%d,%d)" % (self.start, self.stop, self.step)

    # NB: len(self) will convert this to an int, and may fail
    def __len__(self):
        return (self.stop - self.start)//(self.step)

    def __getitem__(self, key):
        if key < 0:
            key = self.__len__() + key
            if key < 0:
                raise IndexError("list index out of range")
            return self[key]
        n = self.start + self.step*key
        if cmp(n, self.stop) != cmp(0, self.step):
            raise IndexError("list index out of range")
        return n

    def __reversed__(self):
        return MyXRange(self.stop-self.step, self.start-self.step, -self.step)

    def __contains__(self, val):
        if val == self.start: return cmp(0, self.step) == cmp(self.start, self.stop)
        if cmp(self.start, val) != cmp(0, self.step): return False
        if cmp(val, self.stop) != cmp(0, self.step): return False
        return (val - self.start) % self.step == 0