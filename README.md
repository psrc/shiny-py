# Shiny for Python

- `pip install shiny`
- There is core vs express versions of Shiny Python. Express has limited capabilities

- Use `breakpoint()` to debug
- The difference
    - `reactive.effect` is equivalent to `observe` in R; triggers immediately
    - `reactive.calc` is equivalent to `reactive` in R; lazy eval, requires function to be called to execute
    - https://shiny.posit.co/py/api/core/reactive.effect.html

## Deploy

- `pip install rsconnect-python`
- Set up machine with shinyapps credentials:

    - Login to PSRC's shinyapps.io account. 
    - Navigate to Account > Tokens. 
    - Select a token and click 'Show'.
    - Select 'With Python'
    - Show all tokens and secret then 'Copy to clipboard'
    - Paste and run in terminal

- To deploy: `rsconnect deploy shiny C:/Users/CLam/github/shiny-py --name psrcwa --title test-shiny-py1`  
- URL: https://psrcwa.shinyapps.io/test-shiny-py1/