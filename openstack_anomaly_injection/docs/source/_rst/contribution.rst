============
Contribution
============


Implementing new anomalies
==========================

1. Choose anomaly group
------------------------
The new anomaly can belong in one of the three groups: ``network``, ``stress`` and ``system``.

2. Create new anomaly class
---------------------------
When implementing a new anomaly, make sure you create a separate file for the class.

.. note::
    Don't forget to inherit from the base ``Anomaly`` class.

.. code-block:: python

   class PauseAnomaly(Anomaly):
        def __init__(self, params, target, conn, *args, **kwargs):
            supported_targets = ["deployment", "container", "host"]
            name = "Pause"
            super().__init__(params, target, conn, supported_targets=supported_targets, name=name)
            self.class_specific_params = None

.. note::
    - You must specify which targets does the anomaly support in ``supported_targets``. Possible targets are ``deployment``,
      ``host``, ``container``, ``network``.
    - You must specify the ``name`` of the anomaly.


If you want to implement logging, use any of the following loggers:

    .. code-block:: python

        import logging
        log_info = logging.getLogger('infoLog')
        log_error = logging.getLogger('errorLog')
        log_debug = logging.getLogger('debuggerLog')
        log_status = logging.getLogger('statusLog')

3. Implement methods
--------------------
You must implement the following methods:
    - ``_run()`` - This function should contain the logic for implementing the anomaly
    - ``_unpack_params(params)`` - This function should unpack the anomaly-specific parameters from the params dictionary.

.. note::
   - You don't need to implement the arguments for ``delay`` and ``duration``.
   - You don't have to implement the delay functionality as it is already implemented in the base ``Anomaly`` class.

.. code-block:: python

    def _unpack_params(self, params):
        self.duration = convert_time_to_s(params.get('duration', '0s'))
        self.delay = convert_time_to_s(params.get('delay', '0s'))

    def _run(self):
        self.target.stop()
        threading.Timer(self.duration, self.target.start).start()

Every anomaly class receives ``target`` object from ``node_control/api`` folder.
If a target method needs to be implemented, please refer to the `Implement API methods`_

4. Import class to ``__init__.py``
----------------------------------
In the ``__init__.py`` of the new anomaly directory, add the following:
    - import the class
    - add the class to the ``__all__`` list.

.. code-block:: python

    from .pause import PauseAnomaly

    __all__ = ["PauseAnomaly"]

5. Add anomaly in the anomaly injector
--------------------------------------
In the ``anomaly_injection/injector.py`` file add the anomaly to the ``_anomaly_cls`` dictionary


.. code-block:: python

    class AnomalyInjector:
        _anomaly_cls = {"pause": PauseAnomaly, "stress-ng": StressNgAnomaly,"new-anomaly":NewAnomalyClass}

.. note::
    You don't have to import the class in the file if you already imported it in step 3.


6. Create argument parser for the anomaly
-----------------------------------------
In the ``anomaly_injection/config/argparser/<anomaly_group>.py`` file:
    - Add new parser
    - Add arguments to the parser

.. code-block:: python

    # add new parser
    stress_ng_anom = sub_stress.add_parser("stress-ng", parents=[default_args])
    # add arguments
    stress_ng_anom.add_argument("--stressors", type=str, required=True, dest="param_stressors",
                                help="String containing stress-ng params. "
                                     "Eg. \"--cpu 2\". Avoid using '-t' in the stressors string. Instead use the duration"
                                      " parameter of the anomaly to specify duration ")

.. note::
   - You must use ``add_parser()`` in order to create new sub parser.
   - You don't need to implement the arguments for ``delay`` and ``duration``.
   - the ``add_parser()`` method must have the ``parents=[default_args]`` parameter in order to inherit the arguments for
     ``delay`` and ``duration``.




Extend Node Control
===================


Implement API methods
=====================
Implementing API methods is pretty straightforward. When implementing new methods, you only need to pass arguments to the
corresponding driver method. If the driver method is not implemented, please refer to `Implement Driver methods`_

.. code-block:: python

        # Code snippet from node_control/api/host.py
        def stress(self, stressors):
            self.driver.stress(self.ip, stressors)

Implement Driver methods
========================

In order to implement the driver method, you need to prepare ``ansible-playbook`` task as dictionary, define hosts,
and pass the arguments to the ``_run_task()`` method.

.. code-block:: python

    def stress(self, host, stressors):
        task = {
            'shell': {
                'cmd': f'stress-ng ' + stressors
            },
        }
        hosts = [host]
        self._run_task(hosts, task, 'Stress')
