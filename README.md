# CivOmega: Bill Search Module

A simple module for [CivOmega][civomega_repo]. See
[the CivOmega repo][civomega_repo].

* **CivOmega Demo**: http://www.civomega.com/
* **CivOmega Repo**: https://github.com/CivOmega/civomega

[civomega_repo]: https://github.com/CivOmega/civomega

---

This module queries the [Sunlight Foundation](http://sunlightfoundation.com)'s
APIs. When using this module (**note: it's installed in CivOmega by default**)
you'll need to have [an API key](http://sunlightfoundation.com/api/).

Once you have the API key, make sure you do this…

```shell
export SUNLIGHT_API_KEY=$YOUR_KEY_HERE
```

…before running the CivOmega server (`python manage.py runserver`).
