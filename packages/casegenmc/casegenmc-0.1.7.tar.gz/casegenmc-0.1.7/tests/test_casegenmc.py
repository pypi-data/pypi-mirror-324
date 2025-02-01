import casegenmc as cgm 
import numpy as np
cgm.init_casegenmc(setup_tex=False,fontsize=8,figsize=[6,6],parallel=False)

if __name__ == "__main__":


    def model(x):
        out = {}
        out["y0"] = x["x0"]**2 + np.exp(x["x1"]) + x['x3']
        out["y1"] = x["x0"] + x["x1"] + x["x2"] + x["x3"]
        out["y3 a"] = x["x0"] + x["x1"] + x["x2"] + x["x3"]
        return out

    # Dictionary specifying variables with uncertainties
    # mean, unc, unc_range (tolerance or 3 sigma), bounds (minimum and maximum value)
    input_stack = {
        "x0": {"mean": 1., "unc": .2, 'range': [0, 5], 'bounds': [0, 100], 'unc_type': 'normal'},
        "x1": {"mean": 1., "unc": .2, 'range': [0, 3], 'unc_type': 'normal'},
        "x2": 3., "x3": 4, 'x4': 'a',
        "x5": {"mean": "a",  'range': ["a", "b"], "options": ["a", "b", "c"], "unc_type": "choice", },
        "x6": {"mean": "a",   "options": ["a", "b", "c"], "unc_type": "choice", "prob": [.1, .3, .6] },
        "x7": {"mean": "a", 'unc':[.2,.8] ,'range': ["a", "b"], "options": ["a", "b", "c"], "unc_type": "choice", },

    }

    input_stack = cgm.process_input_stack(input_stack)
    print('aaa')
    print(input_stack)

    if 1 == 0:
        # NEORL model

        # split input stack into fixed and variable, based on if unc is 0 or if range is length 1
        fixed_inputs = {k: v["mean"] for k, v in input_stack.items()
                        if len(v["range"]) == 1}
        variable_inputs = {k: v for k,
                           v in input_stack.items() if k not in fixed_inputs}
        par_opt = "y0"
        print("fixed_inputs", fixed_inputs)
        print("variable_inputs", variable_inputs)

        from NEORL_wrap import create_NEORL_funwrap, NEORL_getbounds
        NEORL_model = create_NEORL_funwrap(
            model, par_opt=par_opt, variable_inputs=variable_inputs.keys(), fixed_inputs=fixed_inputs)

        BOUNDS = NEORL_getbounds(variable_inputs)

        # try NEORL model with values within the bounds
        # Generate values within the bounds
        x_values = []
        for key, bound in BOUNDS.items():
            if bound[0] == 'float':
                x_values.append(np.random.uniform(bound[1], bound[2]))
            elif bound[0] == 'int':
                x_values.append(np.random.randint(bound[1], bound[2]))
            elif bound[0] == 'grid':
                x_values.append(np.random.choice(bound[1]))

        print(x_values)

        # Call the NEORL model with the generated values
        result = NEORL_model(x_values)
        print("NEORL model result:", result)

        print("BOUNDS", BOUNDS)

    # run each analysis
    # cgm.run_analysis(model=model, input_stack=input_stack, analyses=["estimate"],  )
    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["estimate_unc"], par_output="y0",plotting=False)
    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["estimate_unc_extreme_combos"],  par_output="y0",save_results=True)



    
    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["sensitivity_analysis_unc"], par_sensitivity=["x0", "x1"], par_grid_xy=["x0", "x1"], par_output="y0")
    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["sensitivity_analysis_range"], par_sensitivity=["x0", "x1"], par_grid_xy=["x0", "x1"], par_output="y0",plotting=True,save_results=True)
    cgm.run_analysis(model, input_stack, 
                     n_samples=10,
                     analyses=["sensitivity_analysis_range"], 
                     par_sensitivity=["x0"],
                     par_sensitivity_range=[(-1.2, 6)],
                     par_output=["y0",'y3 a','y1','x0'],
                     plotting=True,save_results=True)

    cgm.run_analysis(
        model,
        input_stack,
        n_samples=1000,
        analyses=["sensitivity_analysis_2D"],
        par_grid_xy=["x0", "x1"],
        par_output="y0",
        plotting=True,
    )
    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["regular_grid"],  par_output="y0")

    cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["random_uniform_grid"], par_output="y0")
    #
    # cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["GA"], par_sensitivity=["x0", "x1"], par_grid_xy=["x0", "x1"], par_output="y0")
    # cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["population_rankings"], par_sensitivity=["x0", "x1"], par_grid_xy=["x0", "x1"], par_output="y0")
    # cgm.run_analysis(model, input_stack, n_samples=1000, analyses=["sobol_indices"], par_sensitivity=["x0", "x1"], par_grid_xy=["x0", "x1"], par_output="y0")
