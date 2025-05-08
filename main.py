bracket_dict = {
    '(': ')',
    '[': ']',
    '{': '}'
}


class Stack(list):
    def is_empty(self):
        return len(self) == 0

    def push_item(self, item):
        self.append(item)

    def pop_item(self):
        if not self.is_empty():
            item = self[-1]
            self.__delitem__(-1)
            return item

    def peek(self):
        if not self.is_empty():
            return self[-1]

    def size(self):
        return len(self)


def checking_balance(sequence):
    stack = Stack()
    for item in sequence:
        if item in bracket_dict:
            stack.push_item(item)
        elif item == bracket_dict.get(stack.peek()):
            stack.pop_item()
        else:
            return False
    return stack.is_empty()


if __name__ == '__main__':
    balanced_list = [
        '(((([{}]))))',
        '[([])((([[[]]])))]{()}',
        '{{[()]}}'
    ]
    unbalanced_list = [
        '}{}',
        '{{[(])]}}',
        '[[{())}]'
    ]
    for collection in balanced_list + unbalanced_list:
        if checking_balance(collection):
            print(f'{collection:35}{'Сбалансированно'}')
        else:
            print(f'{collection:35}{'Несбалансированно'}')
