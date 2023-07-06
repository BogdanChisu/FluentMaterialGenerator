def write_head_lines(filepath):

    head_text = """;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                                                              ;;;
;;;             Fluent USER DEFINED MATERIAL DATABASE            ;;;
;;;                                                              ;;;
;;; (name type[fluid/solid] (chemical-formula . formula)         ;;;
;;;             (prop1 (method1a . data1a) (method1b . data1b))  ;;;
;;;            (prop2 (method2a . data2a) (method2b . data2b)))  ;;;
;;;                                                              ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(
	(glycol-water-ck24 fluid
		(chemical-formula . #f)
    """
    with open(filepath, 'a') as f:
        f.write(head_text)

def write_end_lines(filepath):
    end_text = """        (molecular-weight (constant . 28.966))
		(characteristic-vibrational-temperature (constant . 2686))
		(lennard-jones-length (constant . 3.711))
		(lennard-jones-energy (constant . 78.59999999999999))
		(thermal-accom-coefficient (constant . 0.9137))
		(velocity-accom-coefficient (constant . 0.9137))
		(formation-entropy (constant . 194336))
		(reference-temperature (constant . 298.15))
		(critical-pressure (constant . 3758000.))
		(critical-temperature (constant . 132.3))
		(acentric-factor (constant . 0.033))
		(critical-volume (constant . 0.002857))
		(electric-conductivity (constant . 1e-09))
		(dual-electric-conductivity (constant . 1e-09))
		(therm-exp-coeff (constant . 0))
		(speed-of-sound (none . #f))
	)

)
    """
    with open(filepath, 'a') as f:
        f.write(end_text)
def add_spaces(a_str):
    return 4 * " " + a_str

def write_var(filepath, source_file, variable_name):

    var_text = '	(' + variable_name + ' (polynomial piecewise-linear '

    with open(source_file, 'r') as f:
        var_lines = f.readlines()
        for line in var_lines:
            if len(line) > 1:
                line = line[:-1]
                var_line = line.split(', ')
                # print(var_line)
                var_text += '('
                var_text += var_line[0]
                var_text += '.  . '
                var_text += var_line[1]
                var_text += ')'
                var_text += ' '

    var_text = var_text[:-1]

    if variable_name == 'density':
        var_text += ') (constant . 1073.35) (compressible-liquid 101325 1073.35 142000. 1 1.1 0.9))'

    elif variable_name == 'specific-heat':
        var_text = add_spaces(var_text)
        var_text += ') (constant . 1006.43) (polynomial piecewise-polynomial (100 1000 1161.48214452351 -2.36881890191577 0.0148551108358867 -5.03490927522584e-05 9.9285695564579e-08 -1.11109658897742e-10 6.54019600406048e-14 -1.57358768447275e-17) (1000 3000 -7069.81410143802 33.7060506468204 -0.0581275953375815 5.42161532229608e-05 -2.936678858119e-08 9.237533169567681e-12 -1.56555339604519e-15 1.11233485020759e-19)) (polynomial nasa-9-piecewise-polynomial (200. 1000. 2898903. -56496.26 1437.799 -1.653609 0.003062254 -2.279138e-06 6.272365e-10) (1000. 6000. 69324940. -361053.2 1476.665 -0.06138349 2.027963e-05 -3.075525e-09 1.888054e-13)))'

    elif variable_name == 'thermal-conductivity':
        var_text = add_spaces(var_text)
        var_text += ') (constant . 0.0242))'

    # viscosity
    else:
        var_text = add_spaces(var_text)
        var_text += ') (constant . 1.7894e-05) (sutherland 1.716e-05 273.11 110.56) (power-law 1.716e-05 273.11 0.666) (blottner-curve-fit 0.0307 0.23 -10.8))'

    with open(filepath, 'a') as f:
        f.write(var_text)
        f.write('\n')


def main():

    ##############################
    ## FILE PATHS ##
    sources_dict ={
        'density': 'input_data/Glycol-Temp-Density_[Kg-m^3].txt',
        'specific-heat': 'input_data/Glycol-Temp-Cp_[J-Kg^-1-K^-1].txt',
        'thermal-conductivity': 'input_data/Glycol-Temp-Lambda_[W-m^-1-K^-1].txt',
        'viscosity': 'input_data/Glycol-Temp-Viscosity_[Pa-s].txt'
    }
    
    destination_file = 'output_data/glycol-water-ck24-auto.scm'

    ##############################
    ## FILE Writing ##
    write_head_lines(destination_file)

    ## FIELD VARS WRITING ##
    for field_var in sources_dict.keys():
        write_var(destination_file, sources_dict[field_var], field_var)

    ## COMPLETE THE FILE ##
    write_end_lines(destination_file)


if __name__ == '__main__':
    main()