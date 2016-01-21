import io

class Fib:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.a = 0
        self.b = 1
        return self
    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a = self.b
        self.b = self.a + self.b
        return fib

def return_new_dictionary(old_function):
    def new_function(*args):
        print('decorator has been run')
        x = old_function(*args)
        return x.clear()
    return new_function


@return_new_dictionary
def pow_to_dictionary(dictionary_arg, power, change_list):
    new_dictionary = dictionary_arg.copy()
    for name, data in new_dictionary.items():
        if name in change_list:
            new_dictionary[name] = pow(data, power)
    return new_dictionary


if __name__ == '__main__':
    list = [10,20,30,40,50]
    dictionary = {'one': 130, 'two': 450, 'three': 7990, 'four': 69983}
    change_list = ['two', 'four']
    new_dict = pow_to_dictionary(dictionary, 10, change_list)
    print(dictionary)
    print('dictionary', id(dictionary))

    print(new_dict)
    print('new dict', id(new_dict))