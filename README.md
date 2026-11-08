# api-blog

Blog API built with Django. The project has two apps: `auths` (custom user with email login) and `blog` (categories, tags, posts, comments).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Seeding

The `seed` command fills the database with fake data (made with Faker).

```bash
python3 manage.py seed
```

### Arguments

| Argument     | Default | Description                              |
|--------------|---------|------------------------------------------|
| `--users`    | 20      | Number of users to create                |
| `--posts`    | 100     | Number of posts to create                |
| `--comments` | 500     | Number of comments to create             |
| `--clear`    | off     | Delete old data before creating new data |

### Examples

```bash
python3 manage.py seed
python3 manage.py seed --users 50 --posts 300 --comments 1500
python3 manage.py seed --clear --users 50 --posts 300 --comments 1500
```

### What it creates

- Users with emails like `name.surname@example.com`. All seeded users have the password `seed12345`. Some users are inactive and some are staff.
- 8 categories and 20 tags.
- Posts with a unique slug, a random author, about 70% published and 30% draft. A few posts have no category. Every post gets from 0 to 5 tags.
- Comments on published posts only.

Everything is created with `bulk_create`. With `--clear`, comments, posts, tags, categories and all non-superuser users are deleted first. Superusers are never deleted.

### Errors

The command stops with an error message when:

- any number is negative (`Numbers must not be negative.`)
- posts or comments are requested but there are no users (`There are no users. Use --users first.`)
- comments are requested but there are no published posts (`There are no published posts.`)

### Output

```
Users: 50 created
Categories: 8 created
Tags: 20 created
Posts: 300 created
Comments: 1500 created
Done in 3.42 seconds
```

## Admin

The admin uses [Django Unfold](https://github.com/unfoldadmin/django-unfold). Open http://127.0.0.1:8000/admin/ and log in with a superuser.

### Dashboard

The main page shows the number of posts, published posts, drafts and comments, and a table with the latest posts.

![Dashboard](docs/screenshots/)

### Sections

- **Posts**: list with colored status, tags, filters (status, category, date range), search, and actions to publish or move posts to draft. The post page has tabs: Content, Relations and Comments.
- **Comments**: list with a date filter and search by text, author email and post title.
- **Categories and Tags**: list with search and automatic slug.
- **Users**: list with filters and search, custom forms for email login.
- **Groups**: Django groups in Unfold style.

![Posts](docs/screenshots/)
![Post page](docs/screenshots/)
![Comments](docs/screenshots/)
![Users](docs/screenshots/)

### Settings

Unfold is configured in the `UNFOLD` dictionary in `settings/base.py`: site title, colors, environment badge, site dropdown, command search (Cmd+K), sidebar and dashboard callback. The callbacks are in `apps/blog/callbacks.py`.
