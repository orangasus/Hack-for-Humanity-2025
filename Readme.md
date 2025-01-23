# Guidelines and Tips

**NB!** We do things through ExtendedUser model, not User model.
It means that generally we don't address user directly, instead we
do ex_user.user, so if for example you want to do sth based on user id,
user ex_user.id - we need User model only for its built-in django functionality,
but our main model is ExtendedUser

<br>

**Good to know**
- ex_user.save() doesn't mean that the user is saved too, what you need is ex_user.user.save()
- ex_user = ExtendedUser(...) doesn't mean that user is created automatically - you need to create+save user instance first, then assign it to ex_user 
- Update through ExtendedUserSerializer does mean user updates as well, cuz we have overridden method in the serializer

<br>

**In Code**
- Pls, if it's an instance of ExtendedUser, then use ex_user; if it's an instance of User - use user
