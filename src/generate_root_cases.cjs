// Local fixed test inputs; third-party circuit and fixtures remain ignored.
const fs = require('fs');
const path = require('path');
const box = path.resolve(__dirname, '../data/proof-sandbox');
const { buildPoseidon } = require(path.join(box, 'mutation-runtime/node_modules/circomlibjs'));
(async () => {
  const poseidon = await buildPoseidon();
  const hash = xs => poseidon.F.toObject(poseidon(xs.map(BigInt)));
  const original = JSON.parse(fs.readFileSync(path.join(box, 'input.json')));
  function root(x) {
    let h = hash([x.devAddr, x.challenge, x.response]);
    x.pathElements.forEach((p,i) => {
      if (!['0','1'].includes(x.pathIndices[i])) throw Error('nonbinary index');
      h = hash(x.pathIndices[i] === '0' ? [h,p] : [p,h]);
    });
    return h.toString();
  }
  if (BigInt(root(original)) !== BigInt(original.root)) throw Error('Original root mismatch');
  const stale = {...original, response:(BigInt(original.response)+1n).toString()};
  const replaced = {...stale, root:root(stale)};
  const invalidSig = {...original, S:(BigInt(original.S)+1n).toString()};
  const cases = {original, stale_root:stale, recomputed_root:replaced, invalid_signature:invalidSig};
  const dest = path.join(box, 'root-binding');
  fs.mkdirSync(dest);
  for (const [name,input] of Object.entries(cases)) {
    fs.writeFileSync(path.join(dest,name+'.json'),JSON.stringify(input,null,2)+'\n');
  }
  console.log(JSON.stringify({original_root_recomputed:true,changed_root:BigInt(replaced.root)!==BigInt(original.root),cases:Object.keys(cases)}));
})().catch(e=>{console.error(e);process.exitCode=1;});
