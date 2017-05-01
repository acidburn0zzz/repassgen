import commandLineArgs from 'command-line-args';
import generate from './generator';

const jsonData = require('./base.json');
const data = jsonData;

const optionDefenitions = [
  { name: 'help', alias: 'h', type: Boolean},
  { name: 'length', alias: 'l', type: Number},
  { name: 'complexity', alias: 'c', type: String},
  { name: 'amount', alias: 'a', type: Number}
];

const options = commandLineArgs(optionDefenitions);

const repassgen = () => generate(options, data);

export default repassgen;
