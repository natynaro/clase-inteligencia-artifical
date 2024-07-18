using System.Text;

namespace busqueda_ciegas_net;

public class Node<T> where T : notnull /*: IComparable<Node>*/
{
    public object Id { get; init; }
    public virtual T State { get; init; }

    public List<Node<T>> Children { get; } = [];

    // public SortedSet<Node> Children { get; private set; } = new(Comparer<Node>.Create((n1, n2) => n1.CompareTo(n2)));
    public Node<T>? Parent { get; private set; }
    public Operator<T>? Operator { get; init; }
    public List<Operator<T>> Operators { get; init; } = [];
    public int Level { get; private set; } = 0;

    public Node<T> Add(object id, T state, Operator<T> @operator)
    {
        var node = new Node<T>
        {
            Id = id,
            State = state,
            Operator = @operator,
            Operators = Operators,
            Level = Level + 1,
            Parent = this
        };
        Children.Add(node);
        return node;
    }

    public Node<T> Add(in Node<T> node)
    {
        node.Level = Level + 1;
        node.Parent = this;
        Children.Add(node);
        return node;
    }

    public IEnumerable<Node<T>> PathToRoot()
    {
        var current = this;
        do
        {
            yield return current;
            current = current.Parent;
        } while (current is not null);
    }

    public bool IsRepeatedInPath(T state)
    {
        // foreach (var node in PathToRoot()) if (node.State.Equals(state)) return true;
        return PathToRoot().Any(node => node.State.Equals(state));
    }

    public IEnumerable<Node<T>> CreateChildren()
    {
        return CreateChildStates().Select(state => new Node<T>
        {
            Operators = Operators,
            State = state,
        });
    }

    public IEnumerable<T> CreateChildStates()
    {
        return Operators.Select(@operator => @operator.Func(State)).Where(state => !IsRepeatedInPath(state));
    }

    public virtual double Cost()
    {
        return 1;
    }

    public virtual double Heuristic()
    {
        return 1;
    }

    public double F()
    {
        return Cost() + Heuristic();
    }

    public override string ToString()
    {
        var builder = new StringBuilder();
        foreach (var node in PathToRoot().Reverse())
        {
            builder.AppendLine(node.Operator is null
                ? node.State.ToString()
                : $"operator: {node.Operator.Name}\t state: {node.State}");
        }

        return builder.ToString();
    }

    // public int CompareTo(Node? other)
    // {
    //     throw new NotImplementedException();
    // }
}

public record Operator<T>(string Name) where T : notnull
{
    public required Func<T, T> Func { get; init; }
}