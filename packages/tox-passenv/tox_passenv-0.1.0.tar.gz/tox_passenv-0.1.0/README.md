# tox-passenv plugin ![CI](https://github.com/stanislavlevin/tox-passenv/workflows/CI/badge.svg)

This is the backport of `tox3` functionality of `TOX_TESTENV_PASSENV` for `tox4`:

> If defined the TOX_TESTENV_PASSENV environment variable (in the tox invocation
  environment) can define additional space-separated variable names that are to
  be passed down to the test command environment.

Usage
-----

```
export TOX_TESTENV_PASSENV='FOO BAR'
tox
```

Note
----

The plugin does nothing if installed for `tox3`.

License
-------

Distributed under the terms of the **MIT** license, `tox-passenv` is
free and open source software.
