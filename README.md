# shiny-py

- `pip install shiny`
- There is core vs express versions of Shiny Python. Express has limited capabilities

- Use `breakpoint()` to debug
- The difference
    - `reactive.effect` is equivalent to `observe` in R; triggers immediately
    - `reactive.calc` is equivalent to `reactive` in R; lazy eval, requires function to be called to execute
    - https://shiny.posit.co/py/api/core/reactive.effect.html