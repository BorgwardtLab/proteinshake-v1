var representation = 'graph';
var framework = 'torch';

const lines = {
    comment_1: {
        graph: '# Convert them to graphs with an epsilon neighborhood of 8 Angstrom',
        voxel: '# Convert them to voxels with a voxelsize of 10 Angstrom',
        point: '# Convert them to point clouds',
    },
    comment_2: {
        pyg: '# Load into PyTorch-Geometric data structures',
        dgl: '# Load into DGL data structures',
        nx: '# Load into NetworkX data structures',
        torch: '# Load into PyTorch data structures',
        tf: '# Load into Tensorflow data structures',
        np: '# Load into Numpy data structures',
    },
    convert: {
        graph: 'graph(eps=8)',
        voxel: 'voxel(voxelsize=10)',
        point: 'point()',
    },
};

function quickstart() {
    var representations = document.getElementById('representations');
    [...representations.children].forEach(x=>x.classList.remove('selected'));
    var selected = document.getElementById(representation);
    selected.classList.add('selected');

    if (representation == 'graph') {
        ['torch','tf','np'].forEach(x=>document.getElementById(x).style.display='none');
        ['pyg','dgl','nx'].forEach(x=>document.getElementById(x).style.display='flex');
        if (['torch','tf','np'].includes(framework)) framework = {torch:'pyg',tf:'dgl',np:'nx'}[framework];
    } else {
        ['torch','tf','np'].forEach(x=>document.getElementById(x).style.display='flex');
        ['pyg','dgl','nx'].forEach(x=>document.getElementById(x).style.display='none');
        if (['pyg','dgl','nx'].includes(framework)) framework = {pyg:'torch',dgl:'tf',nx:'np'}[framework];
    }

    var frameworks = document.getElementById('frameworks');
    [...frameworks.children].forEach(x=>x.classList.remove('selected'));
    var selected = document.getElementById(framework);
    selected.classList.add('selected');

    var code = document.getElementById('code');
    code.innerHTML =
`from proteinshake.tasks import EnzymeClassificationTask
from proteinshake.mocks import MockModel

# Use proteins with enzyme class annotations
${lines.comment_1[representation]}
${lines.comment_2[framework]}
task = EnzymeClassificationTask().to_${lines.convert[representation]}.${framework}()

# Replace this with your own model
model = MockModel(output_shape=task.output_shape)

# Train using native data loaders
for X,y in task.train_loader():
    model.train_step(X) # your model training goes here

# Evaluation with the provided metrics
for X,y in task.test_loader():
    prediction = model.test_step(X)
    metrics = task.evaluate(y, prediction)
    print(metrics)`;
    Prism.highlightAll();
}

window.addEventListener('load', quickstart);
