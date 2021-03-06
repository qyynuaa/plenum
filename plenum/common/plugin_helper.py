import importlib

import os

from plenum.common.util import getConfig
from plenum.common.log import getlogger

pluginsLoaded = {}  # Dict(baseDir, List[plugin names])
pluginsNotFound = {}  # Dict(baseDir, List[plugin names])

logger = getlogger("plugin-loader")


def loadPlugins(baseDir):
    global pluginsLoaded

    alreadyLoadedPlugins = pluginsLoaded.get(baseDir)
    i = 0
    if alreadyLoadedPlugins:
        logger.debug("Plugins {} are already loaded from basedir: {}".format(
            alreadyLoadedPlugins, baseDir))
    else:
        logger.debug(
            "Plugin loading started to load plugins from basedir: {}".format(
                baseDir))

        config = getConfig()
        pluginsDirPath = os.path.expanduser(os.path.join(
            baseDir, config.PluginsDir))

        if not os.path.exists(pluginsDirPath):
            os.makedirs(pluginsDirPath)
            logger.debug("Plugin directory created at: {}".format(
                pluginsDirPath))

        if hasattr(config, "PluginsToLoad"):
            for pluginName in config.PluginsToLoad:
                try:
                    pluginPath = os.path.expanduser(os.path.join(pluginsDirPath,
                                              pluginName + ".py"))
                    if os.path.exists(pluginPath):
                        spec = importlib.util.spec_from_file_location(
                            pluginName,
                            pluginPath)
                        plugin = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(plugin)
                        if baseDir in pluginsLoaded:
                            pluginsLoaded[baseDir].add(pluginName)
                        else:
                            pluginsLoaded[baseDir] = {pluginName}
                        i += 1
                    else:
                        if not pluginsNotFound.get(pluginPath):
                            logger.warn("Note: Plugin file does not exists: {}. "
                                        "Create plugin file if you want to load it"
                                        .format(pluginPath), extra={"cli": False})
                            pluginsNotFound[pluginPath] = "Notified"

                except Exception as ex:
                    # TODO: Is this strategy ok to catch any exception and
                    # just print the error and continue,
                    # or it should fail if there is error in plugin loading
                    logger.warn(
                        "** Error occurred during loading plugin {}: {}"
                            .format(pluginPath, str(ex)))

    logger.debug(
        "Total plugins loaded from basedir {} are : {}".format(baseDir, i))
    return i
