using Graphs
using StatsBase

include("ThresholdModel.jl")
using .ThresholdModel

include("ProfileModel.jl")
using .ProfileModel

include("ProfileThresholdModel.jl")
using .ProfileThresholdModel


function main()
    n = 63392
    m = 13
    k = 3150
    tau = 0.1


    graph = barabasi_albert(n, m)

    infected_counts = ProfileModel.run(
        ProfileModel.State(
            graph,
            Set(StatsBase.sample(1:n, k, replace=false)),
            Set(),
            0.8,
            0,
        ),
        30,
    )
    println(infected_counts)
end

main()
