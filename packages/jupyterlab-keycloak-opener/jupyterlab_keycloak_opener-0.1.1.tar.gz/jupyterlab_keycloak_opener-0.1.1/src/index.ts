import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { usersIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';

const PALETTE_CATEGORY = 'Admin tools';
namespace CommandIDs {
  export const createNew = 'jupyterlab-keycloak-opener:open-keycloak-console';
}

/**
 * Initialization data for the jupyterlab-keycloak-opener extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-keycloak-opener:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ILauncher, ICommandPalette],
  activate: (app: JupyterFrontEnd,
    launcher: ILauncher | null,
    palette: ICommandPalette | null
  ) => {
    console.log('JupyterLab extension jupyterlab-keycloak-opener is activated!');

    let idpserver: string = '';
    requestAPI<any>('idpserver')
      .then(data => {
        idpserver = (data.hasOwnProperty('data')) ? data.data : '';
      })
      .catch(reason => {
        console.error(
          `The jupyterlab_keycloak_opener server extension appears to be missing.\n${reason}`
        );
      });

    const { commands } = app;
    const command = CommandIDs.createNew;

    commands.addCommand(command, {
      label: 'Users',
      caption: 'Users',
      icon: args => (args['isPalette'] ? undefined : usersIcon),
      execute: async args => {
        window.open(
          idpserver,
          '_blank',
          'noreferrer'
        );
      }
    });

    if (launcher) {
      launcher.add({
        command,
        category: 'Admin tools',
        rank: 1
      });
    }

    if (palette) {
      palette.addItem({
        command,
        args: { isPalette: true },
        category: PALETTE_CATEGORY
      });
    }
  }
};

export default plugin;
