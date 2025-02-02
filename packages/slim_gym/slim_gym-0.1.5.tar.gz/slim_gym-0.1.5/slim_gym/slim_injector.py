# -*- coding: utf-8 -*-
"""
@author: nzupp

Creates a SLiM script file for the SFS-based neutral Wright-Fisher simulations
with mutation and a bottleneck
"""

def create_slim_script(output_file, init_mutation_rate, num_sites, recomb_rate, pop_size, sample_size, bottleneck):
    """
    Creates a SLiM script that is SLiM-Gym ready with some custom parameters

    Params:
        output_file (String): Name of the SLiM script the injector generates. Must end with .slim extension.
        init_mutation_rate (Float): Starting mutation rate of the SLiM simulation
        num_sites (Int): Number of sites to simulate (reccomend under 1k for testing)
        recomb_rate (Float): The recombination rate
        pop_size (Int): The size of the starting poplation. Note: Assume Ne = Nc under WF
        sample_size (Int): number of individuals sampled each step
        bottleneck (Float): The multiplicative factor the population is changed by. When less than 1 bottleneck, greater than 1 is expansion
        

    Returns
        Nothing
    """
    
    script = f"""initialize() {{
    defineConstant("FLAG_FILE", "flag.txt");
    initializeMutationRate({init_mutation_rate});
    initializeMutationType("m1", 0.5, "f", 0.0);
    initializeGenomicElementType("g1", m1, 1.0);
    initializeGenomicElement(g1, 0, {num_sites});
    initializeRecombinationRate({recomb_rate});
}}
1 early() {{
    sim.addSubpop("p1", {pop_size});
}}
900:1000 late() {{
    if (community.tick % 10 == 0) {{
        g = p1.sampleIndividuals({sample_size}).genomes;
        g.outputMS("state.txt", append=T);
    }}
}}
1001:5000 early() {{
    if (community.tick % 10 == 0) {{
        newSize = asInteger(p1.individualCount * {bottleneck});
        p1.setSubpopulationSize(newSize);
    }}
}}
1001:5000 late() {{
    if (community.tick % 10 == 0) {{
        g = p1.sampleIndividuals({sample_size}).genomes;
        g.outputMS("state.txt", append=T);
        deleteFile(FLAG_FILE);
        while (fileExists(FLAG_FILE) == F) {{
        }}
        mutValStr = readFile(FLAG_FILE);
        
        while (size(mutValStr) == 0) {{
            mutValStr = readFile(FLAG_FILE);
        }}
        mutVal = asFloat(mutValStr);
        sim.chromosome.setMutationRate(mutVal);
    }}
}}
5001 late() {{
    while (fileExists(FLAG_FILE) == F) {{
    }}
    writeFile("generation_complete.txt", "1");
}}"""

    with open(output_file, 'w') as f:
        f.write(script)