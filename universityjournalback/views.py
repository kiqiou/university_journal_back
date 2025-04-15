from universityjournalback.models import Role, User

admin_role = Role.objects.create(role="Admin")

user = User.objects.create(username="Kate", password="securepassword")

user.role.add(admin_role)

print(User.objects.all())
print(user.role.all())
