

the lookback window within code is just referred to as "window1" and then follow-on period "window2" .... seemed to be the easiest way to not make eyes bleed with variable names.

To run ... cd to this folder and execute main.py ("python3 main.py") ... didn't set this up to pass parameters from cmd line, figured overkill. To change variables or parameters, look in the main function and hopefully everything is clearly commented.

I extended the requirements of the project a bit from what you asked ... can specify any pnl target in absolute or %return terms ... can specify greater than or less than ... can specify overlapping window1 or non-overlapping window1. All of these parameters you can change within the main function.

Seemed to be more appropriate to have the option to make N variable based on total number of strategies in the period since it fluctuates a bit.



