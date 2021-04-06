ALTER TABLE USER
ALTER birth SET DEFAULT '';

DROP TABLE account_emailaddress,
account_emailconfirmation, auth_group,
auth_group_permissions, auth_permission,
auth_user, auth_user_groups, auth_user_user_permissions,
django_admin_log,  django_content_type, django_migrations,
django_session;
