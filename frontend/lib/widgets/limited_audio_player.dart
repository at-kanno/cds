import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';

/// Coordinates exclusive playback across multiple [LimitedAudioPlayer]s.
class ExamAudioCoordinator {
  static final ValueNotifier<String?> activeKey = ValueNotifier<String?>(null);
}

/// Audio player with optional per-clip play limits (matches exercise.html).
class LimitedAudioPlayer extends StatefulWidget {
  const LimitedAudioPlayer({
    super.key,
    required this.url,
    required this.storageKey,
    required this.playCounts,
    this.maxPlays = 0,
    this.enforceLimit = true,
    this.label,
  });

  final String url;
  final String storageKey;
  final Map<String, int> playCounts;
  final int maxPlays;
  final bool enforceLimit;
  final String? label;

  @override
  State<LimitedAudioPlayer> createState() => _LimitedAudioPlayerState();
}

class _LimitedAudioPlayerState extends State<LimitedAudioPlayer> {
  late final AudioPlayer _player;
  bool _inPlaySession = false;
  bool _disabled = false;
  PlayerState _state = PlayerState.stopped;

  int get _plays => widget.playCounts[widget.storageKey] ?? 0;

  bool get _limitActive => widget.enforceLimit && widget.maxPlays > 0;

  @override
  void initState() {
    super.initState();
    _player = AudioPlayer();
    _disabled = _limitActive && _plays >= widget.maxPlays;
    ExamAudioCoordinator.activeKey.addListener(_onActiveChanged);
    _player.onPlayerStateChanged.listen((state) {
      if (!mounted) return;
      setState(() => _state = state);
    });
    _player.onPlayerComplete.listen((_) {
      _inPlaySession = false;
      if (ExamAudioCoordinator.activeKey.value == widget.storageKey) {
        ExamAudioCoordinator.activeKey.value = null;
      }
      if (_limitActive && _plays >= widget.maxPlays) {
        _disable();
      }
    });
  }

  void _onActiveChanged() {
    final active = ExamAudioCoordinator.activeKey.value;
    if (active != null &&
        active != widget.storageKey &&
        _state == PlayerState.playing) {
      _player.pause();
    }
  }

  @override
  void didUpdateWidget(covariant LimitedAudioPlayer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.url != widget.url ||
        oldWidget.storageKey != widget.storageKey) {
      _player.stop();
      _inPlaySession = false;
      _disabled = _limitActive && _plays >= widget.maxPlays;
    }
  }

  @override
  void dispose() {
    ExamAudioCoordinator.activeKey.removeListener(_onActiveChanged);
    if (ExamAudioCoordinator.activeKey.value == widget.storageKey) {
      ExamAudioCoordinator.activeKey.value = null;
    }
    _player.dispose();
    super.dispose();
  }

  Future<void> _disable() async {
    await _player.stop();
    if (!mounted) return;
    setState(() => _disabled = true);
  }

  Future<void> _toggle() async {
    if (_disabled) return;
    if (_state == PlayerState.playing) {
      await _player.pause();
      ExamAudioCoordinator.activeKey.value = null;
      return;
    }

    if (_limitActive && !_inPlaySession) {
      if (_plays >= widget.maxPlays) {
        await _disable();
        return;
      }
      widget.playCounts[widget.storageKey] = _plays + 1;
      _inPlaySession = true;
    }

    ExamAudioCoordinator.activeKey.value = widget.storageKey;
    await _player.play(UrlSource(widget.url));
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    if (_disabled) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Text(
          widget.label == null ? '再生上限に達しました' : '${widget.label}: 再生済み',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.grey.shade600,
              ),
        ),
      );
    }

    final remaining = widget.maxPlays - _plays;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (widget.label != null)
          Text(widget.label!, style: Theme.of(context).textTheme.labelLarge),
        Row(
          children: [
            IconButton(
              onPressed: _toggle,
              icon: Icon(
                _state == PlayerState.playing
                    ? Icons.pause_circle_filled
                    : Icons.play_circle_filled,
              ),
              iconSize: 40,
            ),
            if (_limitActive)
              Text(
                '残り $remaining / ${widget.maxPlays} 回',
                style: Theme.of(context).textTheme.bodySmall,
              ),
          ],
        ),
      ],
    );
  }
}
