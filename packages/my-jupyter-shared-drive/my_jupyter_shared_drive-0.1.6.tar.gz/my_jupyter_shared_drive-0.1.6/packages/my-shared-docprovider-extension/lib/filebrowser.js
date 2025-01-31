/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
import { ILabShell, IRouter, JupyterFrontEnd } from '@jupyterlab/application';
import { IDefaultFileBrowser, IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { YFile, YNotebook } from '@jupyter/ydoc';
import { ICollaborativeDrive } from '@jupyter/collaborative-drive';
import { MySharedDrive } from '@jupyter/my-shared-docprovider';
/**
 * The command IDs used by the file browser plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openPath = 'filebrowser:open-path';
})(CommandIDs || (CommandIDs = {}));
/**
 * The shared drive provider.
 */
export const drive = {
    id: '@jupyter/docprovider-extension:drive',
    description: 'The default collaborative drive provider',
    provides: ICollaborativeDrive,
    optional: [ITranslator],
    activate: (app, translator) => {
        translator = translator !== null && translator !== void 0 ? translator : nullTranslator;
        const trans = translator.load('my-jupyter-shared-drive');
        const drive = new MySharedDrive(app, trans);
        app.serviceManager.contents.addDrive(drive);
        return drive;
    }
};
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export const yfile = {
    id: '@jupyter/my-shared-docprovider-extension:yfile',
    description: "Plugin to register the shared model factory for the content type 'file'",
    autoStart: true,
    requires: [ICollaborativeDrive],
    optional: [],
    activate: (app, drive) => {
        const yFileFactory = () => {
            return new YFile();
        };
        drive.sharedModelFactory.registerDocumentFactory('file', yFileFactory);
    }
};
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export const ynotebook = {
    id: '@jupyter/my-shared-docprovider-extension:ynotebook',
    description: "Plugin to register the shared model factory for the content type 'notebook'",
    autoStart: true,
    requires: [ICollaborativeDrive],
    optional: [ISettingRegistry],
    activate: (app, drive, settingRegistry) => {
        let disableDocumentWideUndoRedo = true;
        // Fetch settings if possible.
        if (settingRegistry) {
            settingRegistry
                .load('@jupyterlab/notebook-extension:tracker')
                .then(settings => {
                const updateSettings = (settings) => {
                    var _a;
                    const enableDocWideUndo = settings === null || settings === void 0 ? void 0 : settings.get('experimentalEnableDocumentWideUndoRedo').composite;
                    disableDocumentWideUndoRedo = (_a = !enableDocWideUndo) !== null && _a !== void 0 ? _a : true;
                };
                updateSettings(settings);
                settings.changed.connect((settings) => updateSettings(settings));
            });
        }
        const yNotebookFactory = () => {
            return new YNotebook({
                disableDocumentWideUndoRedo
            });
        };
        drive.sharedModelFactory.registerDocumentFactory('notebook', yNotebookFactory);
    }
};
/**
 * The shared file browser factory provider.
 */
export const mySharedFileBrowser = {
    id: 'my-jupyter-shared-drive:mySharedFileBrowser',
    description: 'The shared file browser factory provider',
    autoStart: true,
    provides: IDefaultFileBrowser,
    requires: [ICollaborativeDrive, IFileBrowserFactory],
    optional: [IRouter, JupyterFrontEnd.ITreeResolver, ILabShell, ITranslator],
    activate: async (app, drive, fileBrowserFactory, router, tree, labShell, translator) => {
        const { commands } = app;
        const trans = (translator !== null && translator !== void 0 ? translator : nullTranslator).load('jupyterlab');
        app.serviceManager.contents.addDrive(drive);
        // Manually restore and load the default file browser.
        const defaultBrowser = fileBrowserFactory.createFileBrowser('filebrowser', {
            auto: false,
            restore: false,
            driveName: drive.name
        });
        defaultBrowser.node.setAttribute('role', 'region');
        defaultBrowser.node.setAttribute('aria-label', trans.__('File Browser Section'));
        void Private.restoreBrowser(defaultBrowser, commands, router, tree, labShell);
        return defaultBrowser;
    }
};
var Private;
(function (Private) {
    /**
     * Restores file browser state and overrides state if tree resolver resolves.
     */
    async function restoreBrowser(browser, commands, router, tree, labShell) {
        const restoring = 'jp-mod-restoring';
        browser.addClass(restoring);
        if (!router) {
            await browser.model.restore(browser.id);
            await browser.model.refresh();
            browser.removeClass(restoring);
            return;
        }
        const listener = async () => {
            router.routed.disconnect(listener);
            const paths = await (tree === null || tree === void 0 ? void 0 : tree.paths);
            if ((paths === null || paths === void 0 ? void 0 : paths.file) || (paths === null || paths === void 0 ? void 0 : paths.browser)) {
                // Restore the model without populating it.
                await browser.model.restore(browser.id, false);
                if (paths.file) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.file,
                        dontShowBrowser: true
                    });
                }
                if (paths.browser) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.browser,
                        dontShowBrowser: true
                    });
                }
            }
            else {
                await browser.model.restore(browser.id);
                await browser.model.refresh();
            }
            browser.removeClass(restoring);
            if (labShell === null || labShell === void 0 ? void 0 : labShell.isEmpty('main')) {
                void commands.execute('launcher:create');
            }
        };
        router.routed.connect(listener);
    }
    Private.restoreBrowser = restoreBrowser;
})(Private || (Private = {}));
