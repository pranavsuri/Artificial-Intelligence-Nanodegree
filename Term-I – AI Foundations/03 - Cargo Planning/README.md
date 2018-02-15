# Implementing a Planning Search
> A planning agent was implemented to solve deterministic logistics-planning problems for an air cargo transport system. The underlying logic makes use of a planning graph and A* search with automatically generated heuristics. The results/performance are then compared against several uninformed non-heuristic search methods (BFS, DFS, etc.)

## About
The template code is available at https://github.com/udacity/AIND-Planning.

**Reading reference:** "Artificial Intelligence: A Modern Approach" 3rd edition chapter 10 or 2nd edition chapter 11 on 'Planning,' sections:
- The Planning Problem
- Planning with State-Space Search

available on the [AIMA book site](http://aima.cs.berkeley.edu/2nd-ed/newchap11.pdf).

Given were classical PDDL (Planning Domain Definition Language) problems. All problems are in the Air Cargo domain. They have the same action schema defined, but different initial states and goals.

Progression-planning problems can be solved with graph searches such as breadth-first, depth-first, and A*, where the nodes of the graph are "states" and edges are "actions." A "state" is the logical conjunction of all boolean ground "fluents," or state variables, that are possible for the problem using Propositional Logic.

- **Uniformed Search Strategies:** These strategies (a.k.a., blind search) have no additional information about states beyond those provided in the problem definition. All they can do is generate successors and distinguish a goal state from a non-goal state.

- **Informed (Heuristic) Search Strategies:** Informed search strategy are the ones that use problem-specific knowledge beyond the definition of the problem itself and can find solutions more efficiently than can an uninformed strategy.

Both uninformed and heuristic-based search were applied to solve the problems and were then compared in an analysis. The study documents the results obtained from each search type to find an optimal solution for each air cargo problem that is; a search algorithm that finds the lowest path among all possible paths from start to goal with a suitable computational cost.

- **Air Cargo Action Schema**
  ```
  Action(Load(c, p, a),
    PRECOND: At(c, a) ∧ At(p, a) ∧ Cargo(c) ∧ Plane(p) ∧ Airport(a)
      EFFECT: ¬ At(c, a) ∧ In(c, p))

  Action(Unload(c, p, a),
      PRECOND: In(c, p) ∧ At(p, a) ∧ Cargo(c) ∧ Plane(p) ∧ Airport(a)
      EFFECT: At(c, a) ∧ ¬ In(c, p))

  Action(Fly(p, from, to),
      PRECOND: At(p, from) ∧ Plane(p) ∧ Airport(from) ∧ Airport(to)
      EFFECT: ¬ At(p, from) ∧ At(p, to))
    ```

- **Problem 1: Initial State and Goal**
  ```
  Init(At(C1, SFO) ∧ At(C2, JFK)
        ∧ At(P1, SFO) ∧ At(P2, JFK)
        ∧ Cargo(C1) ∧ Cargo(C2)
        ∧ Plane(P1) ∧ Plane(P2)
        ∧ Airport(JFK) ∧ Airport(SFO))
  Goal(At(C1, JFK) ∧ At(C2, SFO))

  ```

  The goal above can be reached using different plans, but the **optimal plan length is 6 actions**. Below is a sample plan with optimal length:
  ```
  Load(C1, P1, SFO)
  Load(C2, P2, JFK)
  Fly(P1, SFO, JFK)
  Fly(P2, JFK, SFO)
  Unload(C1, P1, JFK)
  Unload(C2, P2, SFO)
  ```

- **Problem 2: Initial State and Goal**
  ```
  Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL)
      ∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL)
      ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
      ∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
      ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
  Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))
  ```

  Here too, Problem 2's goal can be reached using different plans, but the **optimal plan length is 9 actions**, one of which is shown below:
  ```
  Load(C1, P1, SFO)
  Load(C2, P2, JFK)
  Load(C3, P3, ATL)
  Fly(P1, SFO, JFK)
  Fly(P2, JFK, SFO)
  Fly(P3, ATL, SFO)
  Unload(C3, P3, SFO)
  Unload(C2, P2, SFO)
  Unload(C1, P1, JFK)
  ```

- **Problem 3: Initial State and Goal**
  ```
  Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD)
        ∧ At(P1, SFO) ∧ At(P2, JFK)
        ∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
        ∧ Plane(P1) ∧ Plane(P2)
        ∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
  Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
  ```
  For Problem 3, the **optimal plan length is 12 actions**. Here's a sample plan that is optimal:

  ```
  Load(C1, P1, SFO)
  Load(C2, P2, JFK)
  Fly(P1, SFO, ATL)
  Load(C3, P1, ATL)
  Fly(P2, JFK, ORD)
  Load(C4, P2, ORD)
  Fly(P1, ATL, JFK)
  Fly(P2, ORD, SFO)
  Unload(C4, P2, SFO)
  Unload(C3, P1, JFK)
  Unload(C2, P2, SFO)
  Unload(C1, P1, JFK)
  ```

## Requirements
This project requires **Python 3**. It is recommended to use [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.

## Files
- `my_air_cargo_problems.py` – Air Cargo Transport code.

- `my_planning_graph.py` – Planning-graph code.

- `heuristic_analysis.pdf` – Heuristic analysis report.

- `research_review.pdf` – This one-page report highlights selected important historical developments in the field of AI planning and search and highlights the relationships between the developments and their impact on the field of AI as a whole.

## Testing
- The tests directory includes unittest test cases provided by @udacity to evaluate the implementations. All tests were passed before the project was submitted for review.

  - `python -m unittest tests.test_my_air_cargo_problems`

  - `python -m unittest tests.test_my_planning_graph`

  - All the test cases with additional context by running `python -m unittest -v`

- The `run_search.py` script is for gathering metrics for various search methods on any of the problems.

## Improving Execution Time
The exercises in this project can take a long time to run (from several seconds to several hours) depending on the heuristics and search algorithms, as well as the efficiency of the code. One option to improve execution time is to try installing and using `pypy3` – a python JIT, which can accelerate execution time substantially. This is, however, untested.

## License
[Modified MIT License © Pranav Suri](/License.txt)

I'm grateful to [@philferriere](https://github.com/philferriere/aind-projects) for posting his work online. His analysis on the same project helped me a lot to write this Read-Me in the current form.
