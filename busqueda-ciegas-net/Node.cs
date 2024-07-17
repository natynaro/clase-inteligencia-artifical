namespace busqueda_ciegas_net;

public class Node
{
    public object State { get; private set; }
    public object Value { get; private set; }
    public List<Node> Children { get; private set; } = [];
    public Node? Parent { get; set; }
    public OperatorDelegate? Operator { get; private set; }
    public List<OperatorDelegate> Operators { get; private set; } = [];
    public object Objective { get; private set; }
    public int Level { get; private set; }

    public delegate Node OperatorDelegate(Node node);
}