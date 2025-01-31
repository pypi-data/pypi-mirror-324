// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module my-shared-drive-extension
 */

import { JupyterFrontEndPlugin } from '@jupyterlab/application';

import { drive, yfile, ynotebook, mySharedFileBrowser } from './filebrowser';

/**
 * Export the plugins as default.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [
  drive,
  yfile,
  ynotebook,
  mySharedFileBrowser
];

export default plugins;
