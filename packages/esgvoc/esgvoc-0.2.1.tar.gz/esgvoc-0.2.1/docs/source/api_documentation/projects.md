# Projects

## Term validation

```{eval-rst}
.. note::
  Values are validated against the DRS name of the terms of the projects (not their id, unlike of find functions).
```

```{eval-rst}
.. automodule:: esgvoc.api.projects
   :members: valid_term, valid_term_in_all_projects, valid_term_in_collection, valid_term_in_project
   :member-order: groupwise
```

## Validation reporting

```{eval-rst}
.. automodule:: esgvoc.api.report
   :members:
   :inherited-members: BaseModel
   :member-order: groupwise
```

## Get terms

```{eval-rst}
.. note::
  List the terms, collections and projects.
```

```{eval-rst}
.. automodule:: esgvoc.api.projects
   :members: get_all_collections_in_project, get_all_projects, get_all_terms_in_all_projects, get_all_terms_in_collection, get_all_terms_in_project
   :member-order: groupwise
```

## Find terms

```{eval-rst}
.. note::
  Find functions are based on the id of the terms (not their DRS name, unlike of validation functions).
```

```{eval-rst}
.. automodule:: esgvoc.api.projects
   :members: find_collections_in_project, find_project, find_terms_from_data_descriptor_in_all_projects, find_terms_from_data_descriptor_in_project, find_terms_in_all_projects, find_terms_in_collection, find_terms_in_project
   :member-order: groupwise
```

## Search settings

```{eval-rst}
.. automodule:: esgvoc.api.search
   :members:
   :member-order: groupwise
```
```{eval-rst}
.. autoclass:: esgvoc.core.db.models.mixins.TermKind
   :members:
   :member-order: groupwise
```