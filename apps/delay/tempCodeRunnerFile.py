from faker.providers.lorem.en_US import Provider
# f = Faker()
p = Provider('en_US')
r =  p.text()
print(r)
