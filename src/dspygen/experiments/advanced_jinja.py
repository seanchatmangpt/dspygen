from dspygen.typetemp.environment.typed_environment import environment as env


def main():
    template = env.get_template('hello.j2')
    output = template.render(name='Alice', items=['apple', 'banana'])
    print(output)
    print('main')



if __name__ == '__main__':
    main()
