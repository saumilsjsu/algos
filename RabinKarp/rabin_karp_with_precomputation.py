#python2
from random import randrange
from sys import stdout
class RabinKarp(object):
    def __init__(self, x, a, b, m=1000):
        self.x=x
        self.a=a
        self.b=b
        self.m=m
        self.poly_hash=PolyHash(x, a, b)
     
    def hash_of_previous(self, prev_s, next_s, next_s_hash):
        prev_s_hash=ord(prev_s[0])+self.x*(next_s_hash)-(ord(next_s[len(next_s)-1])*(self.x**(len(next_s))))
#         print(prev_s_hash)
        return prev_s_hash, self.poly_hash.integer_hash(prev_s_hash, self.m)
        
    def is_equal(self,s1, s2):
        if(len(s1)!=len(s2)):
            return False
        for i in range(len(s1)-len(s2)+1):
            for j in range(len(s2)):
                if(s1[i+j]!=s2[j]):
                    return False
        return True
    
    def naive(self, s, p):
        solutions=[]
        if(s==p):
            solutions.append(0)
        pattern_hash=self.poly_hash.poly_hash_with_cardinality_fix(p, self.m)
        for i in range(len(s)-len(p), 0, -1):
            temp_str=s[i:i+len(p)]
            iter_hash=self.poly_hash.poly_hash_with_cardinality_fix(temp_str, self.m)
            if(pattern_hash==iter_hash):
#                 print()
                if(self.is_equal(temp_str, p)):
                    solutions.append(i)
        return solutions
    
    def rabin_karp_with_precomputation(self, s, p):
        solutions_arr=[]
        p_poly_hash=self.poly_hash.poly_hash_with_cardinality_fix(p, self.m)
#         print(p_poly_hash)
        init_hash=self.poly_hash.poly_hash(s[len(s)-len(p):len(s)])
        temp_poly_hash_without_cardinality=init_hash
        init_hash_with_cardinality=self.poly_hash.integer_hash(init_hash, self.m)
        if(init_hash_with_cardinality==p_poly_hash):
            if(self.is_equal(s[len(s)-len(p):len(s)], p)):
                solutions_arr.append(len(s)-len(p))
#         print(s[len(s)-len(p):len(s)], init_hash)
        temp_poly_hash=init_hash
        for i in range(len(s)-len(p)-1, -1, -1):
            if(temp_poly_hash==p_poly_hash):
                if(self.is_equal(p, s[i+1:i+1+len(p)])):
                    solutions_arr.append(i+1)
            temp_poly_hash_without_cardinality, temp_poly_hash=self.hash_of_previous(s[i:i+len(p)], s[i+1:i+len(p)+1], temp_poly_hash_without_cardinality)
#             print(i, s[i:i+len(p)], s[i+1:i+len(p)+1], temp_poly_hash)
        if(temp_poly_hash==p_poly_hash):
            if(self.is_equal(p, s[0:len(p)])):
                solutions_arr.append(0)
        return solutions_arr
            
    
    def precomputation(self, s, p):
        solutions=[]
        pattern_hash=self.poly_hash.poly_hash_with_cardinality_fix(p, self.m)
        for i in range(len(s)-len(p), 0, -1):
            temp_str=s[i:i+len(p)]
            iter_hash=self.poly_hash.poly_hash_with_cardinality_fix(temp_str, self.m)
            if(pattern_hash==iter_hash):
                if(self.is_equal(temp_str, p)):
                    solutions.append(i)
        return solutions
    
    def stress_test(self, min_length_str, max_length_str, min_length_p, max_length_p, min_ascii_in_str, max_ascii_in_str):
        while(True):
            string_len=randrange(min_length_str, max_length_str)
            pattern_len=randrange(min_length_p, max_length_p)
            string=''
            pattern=''
            for i in range(string_len):
                string=string+chr(randrange(min_ascii_in_str, max_ascii_in_str))
                pattern=pattern+chr(randrange(min_ascii_in_str, max_ascii_in_str))

            print(string, pattern)
            if(self.naive(string, pattern)!=self.rabin_karp_with_precomputation(string, pattern)):
                print('FAILED AT '+string+' '+pattern)
                return

class PolyHash(object):
    def __init__(self, x, a, b):
        self.x=x
        self.a=a
        self.b=b
    
    def poly_hash(self, s, p=1299721):
        sum_hash=0
        x=self.x
        for i in range(len(s)-1, -1, -1):
            sum_hash=(sum_hash*x)+ord(s[i])%p
        return sum_hash

    def integer_hash(self, i, m):
        a=self.a
        b=self.b
        return (a*i+b)%m

    def poly_hash_with_cardinality_fix(self, s, m):
        a=self.a
        b=self.b
        x=self.x
        temp=self.poly_hash(s)
#         print('temp=',temp)
        return self.integer_hash(temp, m)

    def get_poly_hash_array(self, s, m=1000):
        for i in range(len(s)):
            s[i]=poly_hash_with_cardinality_fix(s[i], m)
        return s

def problem():
    x=3
    a=4
    b=5
    m=1000
    pattern=raw_input()
    string=raw_input()
    r=RabinKarp(x,a,b,m)
    temp=r.rabin_karp_with_precomputation(string, pattern)
    for i in range(len(temp)-1, -1, -1):
        stdout.write(str(temp[i]))
        stdout.write(' ')
    stdout.write('\n')

problem()
