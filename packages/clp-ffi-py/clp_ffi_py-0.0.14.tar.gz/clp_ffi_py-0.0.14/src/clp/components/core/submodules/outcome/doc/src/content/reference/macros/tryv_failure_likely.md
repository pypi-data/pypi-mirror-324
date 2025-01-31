+++
title = "`OUTCOME_TRYV_FAILURE_LIKELY(expr)/OUTCOME_TRY_FAILURE_LIKELY(expr)`"
description = "Evaluate an expression which results in an understood type, continuing execution if successful, immediately returning `try_operation_return_as(X)` from the calling function if unsuccessful."
+++

Evaluate an expression which results in a type matching the following customisation points, continuing execution if successful, immediately returning {{% api "try_operation_return_as(X)" %}} from the calling function if unsuccessful:

- `OUTCOME_V2_NAMESPACE::`{{% api "try_operation_has_value(X)" %}}
- `OUTCOME_V2_NAMESPACE::`{{% api "try_operation_return_as(X)" %}}
- `OUTCOME_V2_NAMESPACE::`{{% api "try_operation_extract_value(X)" %}}

Default overloads for these customisation points are provided. See [the recipe for supporting foreign input to `OUTCOME_TRY`]({{% relref "/recipes/foreign-try" %}}).

The difference between the `OUTCOME_TRYV(expr)` and `OUTCOME_TRY(expr)` editions is that the latter will set a variable if two or more macro arguments are present (see {{% api "OUTCOME_TRY(var, expr)" %}}). The former requires the `T` to be `void`.

Hints are given to the compiler that the expression will be unsuccessful. If you expect success, you should use {{% api "OUTCOME_TRYV(expr)" %}} instead.

An internal temporary to hold the value of the expression is created, which generally invokes a copy/move. [If you wish to never copy/move, you can tell this macro to create the internal temporary as a reference instead.]({{% relref "/tutorial/essential/result/try_ref" %}})

*Overridable*: Not overridable.

*Definition*: Firstly the expression's temporary is bound to a uniquely named, stack allocated, `auto &&`. If that reference's bound object's `try_operation_has_value()` is false, immediately execute `return try_operation_return_as(propagated unique reference);`, propagating the rvalue/lvalue/etc-ness of the original expression.

*Header*: `<outcome/try.hpp>`
